from ..stores.identified_document import IdentifiedDocumentStore
from ..documents.loader import load_yaml_document


class YamlDocumentStore(object):
    @classmethod
    def load(cls, identity):
        # todo: add back in loader context
        return load_yaml_document(IdentifiedDocumentStore.use(identity))
