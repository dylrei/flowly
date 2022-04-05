from ..constants.runtime import IdentityConfigsKey
from ..constants.versioned_document import IdentifierDelimeter
from ..runtime import IdentityConfigs

_executors = {}

class IdentifiedExecutorStore(object):
    @classmethod
    def validate(cls, identity, fx):
        dotted_identity_domain = identity.split(IdentifierDelimeter.DOMAIN)[0].replace('/', '.')
        method_namespace = fx.__module__
        # function must be identified in the directory structure matching the domain,
        if not method_namespace.endswith(dotted_identity_domain):
            raise RuntimeError(f'Executor identity does not match location of executor declaration: '
                               f'Identity: {identity}; Declaration location: {method_namespace}')
        # domain directory structure must be contained within global content_root
        content_root = IdentityConfigs.get(IdentityConfigsKey.CONTENT_ROOT)
        if not method_namespace.startswith(content_root):
            raise RuntimeError(f'Executor {identity} declared outside of content root {content_root}')

    @classmethod
    def register(cls, identity, fx):
        global _executors
        cls.validate(identity, fx)
        _executors.setdefault(identity, fx)

    @classmethod
    def use(cls, identity):
        if identity not in _executors:
            raise RuntimeError(f'No such registered identity: {identity}')
        return _executors[identity]
