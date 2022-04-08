from ..constants.tags import TagName


class MethodExecutor(object):
    def __init__(self, identity, loaded_yaml):
        self._identity = identity
        self._loaded_yaml = loaded_yaml

    @property
    def identity(self):
        return self._identity

    @property
    def meta_section(self):
        return self._loaded_yaml[TagName.META].value

    @property
    def input_section(self):
        return self._loaded_yaml[TagName.INPUT].value

    @property
    def body_section(self):
        return self._loaded_yaml[TagName.BODY].value

    @property
    def return_section(self):
        return self._loaded_yaml[TagName.RETURN].value

    # def run_payload(self, payload, state=None):
    #     for step_obj in self.body_section:
    #         print(step_obj)
    #     pass