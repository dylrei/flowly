import uuid
from copy import deepcopy

from ..constants.tags import TagName
from ..utils.method import handle_method_or_step_body, render_tag_payload, provide_return, StepReturnData


class Data(object):
    def __init__(self, method_identity, data=None):
        self.identity = str(uuid.uuid4())
        self.method_id = method_identity
        self._value = deepcopy(data) if data is not None else dict()

    def update(self, new_data):
        self._value.update(new_data)

    def __getitem__(self, item):
        if item not in self._value:
            import ipdb; ipdb.set_trace()
        return self._value[item]

    def __setitem__(self, key, value):
        raise RuntimeError(f'You may not set values directly on {self.__class__.__name__}, use '
                           f'update() instead')

    def keys(self):
        return self._value.keys()


class State(Data):
    node = None

    def persist(self):
        pass


class MethodExecutor(object):
    def __init__(self, identity, loaded_yaml):
        self._identity = identity
        self._loaded_yaml = loaded_yaml

    @property
    def identity(self):
        return self._identity

    @property
    def meta_section(self):
        return self._loaded_yaml[TagName.META]._value

    @property
    def input_section(self):
        return self._loaded_yaml[TagName.INPUT]._value

    @property
    def body_section(self):
        return self._loaded_yaml[TagName.BODY]._value

    @property
    def return_section(self):
        if self._loaded_yaml.get(TagName.RETURN):
            return self._loaded_yaml[TagName.RETURN]._value

    def sanity_check(self, data, state):
        pass

    def validate_input(self, data):
        pass

    # "state" is data that persists across multiple Steps in the Run, it corresponds to the !State tag
    # "data" is data that is only available during the lifetime of this Step, it corresponds to the !Data tag
    def run(self, data=None, state=None):
        load_state = False
        if state is not None:
            # if we've got it, we will want to resume where we left off, either here or in the step that last returned
            # to us
            load_state = True
            import ipdb; ipdb.set_trace()
        data = Data(data=data, method_identity=self.identity)
        state = State(data=state, method_identity=self.identity)
        self.sanity_check(data, state)
        self.validate_input(data)
        if load_state:
            if state.method_id == self.identity:
                next_steps = body_advanced_to_node(self.body_section, state.node)
            else:
                # load that method with the state it returned
                pass
        result = handle_method_or_step_body(self.body_section, data, state)
        if isinstance(result, StepReturnData):
            return_data = {
                'method': self.identity,
                'result': result.data,
                'state': state.identity,
                'completed': False,
            }
        else:
            return_data = {
                'method': self.identity,
                'result': render_tag_payload(self.return_section, data, state),
                'state': state.identity,
                'completed': True,
            }
        state.update({'latest_return': return_data})
        return provide_return(return_data, state)



