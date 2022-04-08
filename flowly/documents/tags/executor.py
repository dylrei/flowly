from .base import YAMLConfiguredObject
from ...constants.tags import TagName
from ...stores.identified_executor import IdentifiedExecutorStore


class ActionTag(YAMLConfiguredObject):
    tag_name = TagName.Action
    return_value = None
    non_kwarg_keys = set(['id', 'store_return'])

    @property
    def store_return(self):
        return self.value.get('store_return')

    def kwargs(self):
        return {k: v for k, v in self.value.items() if k not in self.non_kwarg_keys}

    def execute(self):
        executor = IdentifiedExecutorStore.use(self.value['id'])
        self.return_value = executor(**self.kwargs())
        if self.store_return:
            return {self.store_return.tag: {self.store_return.value: self.return_value}}


class MethodTag(YAMLConfiguredObject):
    tag_name = TagName.Method


class ValidatorTag(YAMLConfiguredObject):
    tag_name = TagName.Validator

    def validate(self, node):
        from ...stores.input_validation import InputValidatorStore
        validator = InputValidatorStore.get_validator(self.value['id'])
        return validator.validate(node)
