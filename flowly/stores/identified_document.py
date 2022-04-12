from ..constants.identity import MetaSectionKey
from ..constants.tags import TagName
from ..documents.loader import load_yaml_document
from ..utils.identity import deconstruct_identity, path_for_identity

_documents = {}


class IdentifiedDocumentStore(object):
    @classmethod
    def validate(cls, identity, document):
        loaded_document = load_yaml_document(document)  # TODO: document loading context
        identity_domain = deconstruct_identity(identity)[MetaSectionKey.DOMAIN]
        document_domain = loaded_document[TagName.META]._value[MetaSectionKey.DOMAIN]
        # document domain must match identity domain
        if not identity_domain == document_domain:
            raise RuntimeError(f'Document domain does not match domain of identity: '
                               f'Identity: {identity}; Document domain: {document_domain}')

    @classmethod
    def preload(cls, document_identities):
        map(cls.use, document_identities)

    @classmethod
    def use(cls, identity):
        global _documents
        if identity not in _documents:
            try:
                with open(path_for_identity(identity), 'r') as document:
                    new_doc = document.read()
                    cls.validate(identity, new_doc)
                    _documents[identity] = new_doc
            except FileNotFoundError:
                raise RuntimeError(f'No such document: {identity}')
        return _documents[identity]
