from .versioned_document import VersionedDocumentStore
from ..methods.executor import MethodExecutor
from ..tags.loader import load_yaml


class MethodStore(object):
    @classmethod
    def load(cls, identifier, root_path=None):
        return MethodExecutor(
            identifier=identifier,
            loaded_yaml=load_yaml(VersionedDocumentStore.load(identifier, root_path=root_path))
        )