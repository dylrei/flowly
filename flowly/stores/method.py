from flowly.documents.loader import load_yaml_document
from flowly.executors.method import MethodExecutor
from flowly.stores.identified_document import IdentifiedDocumentStore


class MethodStore(object):
    @classmethod
    def load(cls, identity):
        return MethodExecutor(
            identity=identity,
            loaded_yaml=load_yaml_document(IdentifiedDocumentStore.use(identity))
        )