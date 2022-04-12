from datetime import datetime, timezone

from flowly.constants.method import MethodKeyword
from flowly.constants.tags import TagName
from flowly.documents.tags import YAMLConfiguredObject
from flowly.stores.identified_executor import IdentifiedExecutorStore
from flowly.stores.material import MaterialStore, Material, Asset


def handle_method_or_step_body(body, data, state):
    for item in body:
        result = handle_item(item, data, state)
        if isinstance(result, StepReturnData):
            return result


def handle_item(item, data, state):
    return handler_for_tag[item.tag](item, data, state)


def handle_step(step, data, state):
    if not hasattr(step, 'name'):
        import ipdb; ipdb.set_trace()
    state.node = step.name  # New rules: all steps must have names, all names must be unique within the method
    results = handle_method_or_step_body(step._value[MethodKeyword.BODY], data, state)
    if isinstance(results, StepReturnData):
        return results
    if MethodKeyword.RETURN in step.keys():
        return_data = render_tag_payload(step.value[MethodKeyword.RETURN], data, state)
        state.persist()
        return StepReturnData(return_data, state)


def handle_action(action, data, state):
    return run_executor(
        executor=IdentifiedExecutorStore.use(action.identity),  # todo: document loader context
        action_or_method=action,
        data=data,
        state=state
    )


def handle_method(method, data, state):
    from ..stores.method import MethodStore
    return run_executor(
        executor=MethodStore.load(method.identity),  # todo: document loader context
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


def handle_state(state_tag, data, state):
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
    return {
        'method': state.method_id,
        'node': state.node,
        'state': state.identity,
        'data': return_data,
        'timestamp': datetime.now(timezone.utc)
    }


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
        self.id = state.method_id
        self.node = state.node
        self.data = return_data
        self.resume_state = state.identity