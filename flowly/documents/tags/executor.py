from .base import YAMLConfiguredObject
from ...constants.tags import TagName
from ...stores.identified_executor import IdentifiedExecutorStore


class ExecutorTag(YAMLConfiguredObject):
    @property
    def kwargs(self):
        if isinstance(self._value, dict):
            return {k: v for k, v in self._value.items() if k not in self.control_keys}
        else:
            raise RuntimeError('Attempt to use kwargs on tag with an array-shaped value: '
                               '{self.tag} {self.value}')



class ActionTag(YAMLConfiguredObject):
    tag_name = TagName.Action
    return_value = None

    @property
    def value(self):
        return {k: v for k, v in self._value.items() if k not in self.control_keys}

    def execute(self):
        executor = IdentifiedExecutorStore.use(self.identity)
        return_value = executor(**self.value)
        if self.output_target:
            return {self.output_target.tag: {self.output_target.value: return_value}}


class MethodTag(YAMLConfiguredObject):
    tag_name = TagName.Method


class StepTag(YAMLConfiguredObject):
    tag_name = TagName.Step

    @property
    def name(self):
        return self._value['name']

class ValidatorTag(YAMLConfiguredObject):
    tag_name = TagName.Validator

    def validate(self, node):
        from ...stores.input_validation import InputValidatorStore
        validator = InputValidatorStore.get_validator(self._value['id'])
        return validator.validate(node)
