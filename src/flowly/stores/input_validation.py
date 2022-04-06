from .yaml_document import YamlDocumentStore
from ..constants.context import DocumentLoaderContext
from ..executors.validator import InputValidator


class InputValidatorStore(object):
    @classmethod
    def get_validator(cls, identity):
        return InputValidator(
            identity=identity,
            loaded_yaml=YamlDocumentStore.load(identity, context=DocumentLoaderContext.SPECIFICATION)
        )
