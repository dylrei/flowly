from ..constants.tags import MethodSectionName
from ..stores.versioned_document import VersionedDocumentStore
from ..tags.loader import load_yaml


def get_method_executor(identifier):
    return MethodExecutor(
        identifier=identifier,
        loaded_yaml=load_yaml(VersionedDocumentStore.load(identifier))
    )


class MethodExecutor(object):
    def __init__(self, identifier, loaded_yaml):
        self._identifier = identifier
        self._method = loaded_yaml
        self.sanity_check()

    @property
    def identifier(self):
        return self._identifier

    @property
    def meta_section(self):
        # all values in the META section are considered strings, even if (e.g. version) they *could* be represented as floats
        return {k: str(v) for k, v in self._method[MethodSectionName.META].items()}

    @property
    def input_section(self):
        return self._method[MethodSectionName.INPUT]

    @property
    def body_section(self):
        return self._method[MethodSectionName.BODY]

    @property
    def return_section(self):
        return self._method[MethodSectionName.RETURN]

    def sanity_check(self):
        # todo: unpack identifier and confirm it matches meta_section attributes
        pass