import uuid
from copy import deepcopy
from datetime import timezone, datetime

from ..constants.tags import TagName
from ..models import Run
from ..models.state import RunState
from ..utils.method import handle_method_or_step_body, render_tag_payload, provide_return, StepReturnData, \
    load_data_and_state, body_items_after_node


class Data(object):
    def __init__(self, run_obj, data=None, node=None):
        self.identity = str(uuid.uuid4())
        self.run = run_obj
        self.node = node
        if data is not None:
            self.latest_return = data.get('latest_return', {})
            self._value = deepcopy({k: w for k, w in data.items() if k != 'latest_return'})
        else:
            self.latest_return = dict()
            self._value = dict()

    @property
    def value(self):
        return self._value

    @property
    def method_id(self):
        return self.run.method

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
    def persist(self):
        RunState.objects.create(
            identity=self.identity,
            data=self.value,
            run=self.run,
            node=self.node
        )


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

    def run(self, data_provided=None, state_identity=None):
        self.sanity_check(data_provided, state_identity)
        self.validate_input(data_provided)
        run_obj = Run.objects.create(identity=str(uuid.uuid4()), method=self.identity)
        # "state" is data that persists across multiple Steps in the Run, it corresponds to the !State tag
        # "data" is data that is only available during the lifetime of this Step, it corresponds to the !Data tag
        data, state, state_loaded = load_data_and_state(run_obj, data_provided, state_identity)
        if state_loaded:
            if state.method_id == self.identity:
                next_steps = body_items_after_node(self.body_section, state.latest_return['node'])
            else:
                # load that method with the state it returned
                import ipdb; ipdb.set_trace()
                pass
        else:
            next_steps = self.body_section
        result = handle_method_or_step_body(next_steps, data, state)
        if isinstance(result, StepReturnData):
            return_data = {
                'method': self.identity,
                'node': state.node,
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
            run_obj.completed = datetime.now(tz=timezone.utc)
            run_obj.save()
        state.update({'latest_return': return_data})
        return provide_return(return_data, state)



