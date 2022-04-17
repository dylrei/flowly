from datetime import datetime, timezone

from ..constants.method import MethodKeyword
from ..constants.payload import PayloadKey
from ..constants.tags import TagName
from ..documents.tags import YAMLConfiguredObject
from ..models.state import RunState
from ..stores.material import MaterialStore, Material, Asset


def load_data_and_state(run_obj, data_provided, state_identity):
    from ..executors.method import Data, State
    data = Data(run_obj=run_obj, data=data_provided)
    if state_identity is not None:
        try:
            state_obj = RunState.objects.get(identity=state_identity)
        except RunState.DoesNotExist:
            raise RuntimeError(f'No such state identity: {state_identity}')
        state = State(run_obj=run_obj, data=state_obj.data, node=state_obj.node)
        state_loaded = True
    else:
        state = State(run_obj=run_obj)
        state_loaded = False
    return data, state, state_loaded


def handle_method_or_step_body(body, data, state, namespace):
    for item in body:
        result = handle_item(item, data, state, namespace)
        if isinstance(result, StepReturnData):
            return result


def body_items_after_node(body_section, node_name):
    node_idx = None
    for idx, node in enumerate(body_section):
        if getattr(node, 'name', None) == node_name:
            node_idx = idx
            break
    return body_section[node_idx + 1:]


def handle_item(item, data, state, namespace):
    return handler_for_tag[item.tag](item, data, state, namespace)


def handle_step(step, data, state, namespace):
    if not hasattr(step, 'name'):
        raise RuntimeError(f'Step requires a name, none provided')
    state.node = step.name  # New rules: all steps must have names, all names must be unique within the method
    results = handle_method_or_step_body(step._value[MethodKeyword.BODY], data, state, namespace)
    if isinstance(results, StepReturnData):
        return results
    if MethodKeyword.RETURN in step.keys():
        return_data = render_tag_payload(step.value[MethodKeyword.RETURN], data, state)
        return StepReturnData(return_data, state)


def handle_action(action, data, state, namespace):
    return run_executor(
        executor=namespace.get_executor(action.identity),
        action_or_method=action,
        data=data,
        state=state
    )


def handle_method(method, data, state, namespace):
    return run_executor(
        executor=namespace.get_method(method.identity),
        action_or_method=method,
        data=data,
        state=state
    )


def render_object(obj_tag, data, state):
    return render_for_tag[obj_tag.tag](obj_tag.value, data, state)


def load_material_id_or_ids(key_name, data, state):
    if key_name not in state.keys() and key_name not in data.keys():
        raise RuntimeError(f'Attempt to load material(s) or asset(s) from key not found in !State or !Data: {key_name}')
    return state[key_name] if key_name in state.keys() else data[key_name]


def render_material(key_name, data, state):
    return MaterialStore.load_one_material(identity=load_material_id_or_ids(key_name, data, state))


def render_asset(key_name, data, state):
    return MaterialStore.load_one_asset(identity=load_material_id_or_ids(key_name, data, state))


def render_materials(key_name, data, state):
    return MaterialStore.load_many_materials(identities=load_material_id_or_ids(key_name, data, state))


def render_assets(key_name, data, state):
    return MaterialStore.load_many_assets(identities=load_material_id_or_ids(key_name, data, state))


def render_tag_payload(tag, data, state):
    output = dict()
    tag_data_source = tag.items
    if hasattr(tag, 'kwargs'):
        tag_data_source = tag.kwargs
    for key, value in tag_data_source():
        if isinstance(value, YAMLConfiguredObject):
            source_key = value.value
            if value.tag in [TagName.Data, TagName.State]:
                if value.tag == TagName.Data:
                    sources = [data]
                elif value.tag == TagName.State:
                    sources = [state]
                use_source = None
                for source in sources:
                    if source_key in source.keys():
                        use_source = source
                        break
                if use_source:
                    output[key] = use_source[source_key]
                else:
                    if key == MethodKeyword.OUTPUT_TARGET:
                        # we are setting a new key momentarily, but first we have to load the tag
                        # not an error condition, nothing to do
                        pass
                    else:
                        import ipdb; ipdb.set_trace()
                        raise RuntimeError(f'Attempt to read a {value.tag} value that has not already been set; '
                                           f'key: {source_key}')
            elif value.tag in [TagName.Material, TagName.Asset, TagName.Materials, TagName.Assets]:
                output[key] = render_object(value, data, state)
            else:
                raise RuntimeError(f'No render implemented for source {value.tag}')
        else:
            output[key] = value
    return output


def run_executor(executor, action_or_method, data, state):
    exec_kwargs = render_tag_payload(action_or_method, data, state)
    result = executor(**exec_kwargs)
    if result is not None:
        if action_or_method.output_target:
            target_key = action_or_method.output_target.value
            if action_or_method.output_target.tag == TagName.State:
                state.update({target_key: result})
            elif action_or_method.output_target.tag == TagName.Data:
                data.update({target_key: result})
            else:
                raise RuntimeError(f'No defined way to output to tag {action_or_method.output_target.tag}')
        return result


def load_material(material_tag, data, state):
    return Material(material_tag.value, data, state).value


def load_asset(asset_tag, data, state):
    return Asset(asset_tag.value, data, state).value


def handle_state(state_tag, data, state, namespace):
    data_updates = dict()
    for key, value in state_tag.items():
        if isinstance(value, YAMLConfiguredObject):
            source_key = value._value
            if value.tag == TagName.Data:
                data_updates[key] = data[source_key]
            else:
                raise RuntimeError(f'Unexpected tag encountered in !State block: {value.tag}')
        else:
            data_updates[key] = value
    state.update(data_updates)


def provide_return(return_data, state):
    state.persist()
    return dict(return_data, **{PayloadKey.TIMESTAMP: datetime.now(timezone.utc)})


handler_for_tag = {
    TagName.Action: handle_action,
    TagName.Method: handle_method,
    TagName.Step: handle_step,
    TagName.State: handle_state
}
render_for_tag = {
    TagName.Material: render_material,
    TagName.Asset: render_asset,
    TagName.Materials: render_materials,
    TagName.Assets: render_assets
}


class StepReturnData(object):
    def __init__(self, return_data, state):
        self.resume_method = state.method_id
        self.resume_node = state.node
        self.data = return_data
        self.resume_state = state.identity
