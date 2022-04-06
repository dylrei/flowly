from ..stores.identified_document import IdentifiedDocumentStore
from ..tags.loader import load_yaml_document


class YamlDocumentStore(object):
    @classmethod
    def load(cls, identity, context):
        return load_yaml_document(IdentifiedDocumentStore.use(identity), context)
