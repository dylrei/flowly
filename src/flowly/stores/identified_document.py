from ..constants.identity import MetaSectionKey
from ..constants.runtime import IdentityConfigsKey
from ..runtime import IdentityConfigs
from ..utils.identity import deconstruct_identity, path_for_identity
from ..utils.overlap import overlay_paths

_documents = {}


class IdentifiedDocumentStore(object):
    @classmethod
    def validate(cls, identity, document):
        identity_domain = deconstruct_identity(identity)[MetaSectionKey.DOMAIN]
        document_domain = document.meta_section[MetaSectionKey.DOMAIN]
        # document domain must match identity domain
        if not identity_domain == document_domain:
            raise RuntimeError(f'Document domain does not match domain of identity: '
                               f'Identity: {identity}; Document domain: {document_domain}')
        # domain directory structure must be contained within global content_root
        content_root_path = IdentityConfigs.get(IdentityConfigsKey.PATH_TO_CONTENT_ROOT)
        if not overlay_paths(content_root_path, document_domain):
            raise RuntimeError(f'Document {identity} located outside of content root {content_root_path}')

    @classmethod
    def preload(cls, document_identities):
        map(cls.use, document_identities)

    @classmethod
    def use(cls, identity):
        global _documents
        if identity not in _documents:
            try:
                with open(path_for_identity(identity), 'r') as document:
                    _documents[identity] = document.read()
            except FileNotFoundError:
                import ipdb; ipdb.set_trace()
                raise RuntimeError(f'No such document: {identity}')
        return _documents[identity]
