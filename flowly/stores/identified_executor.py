from ..utils.identity import get_dotted_identity

_executors = {}

class IdentifiedExecutorStore(object):
    @classmethod
    def validate(cls, identity, fx):
        dotted_identity_domain = get_dotted_identity(identity)
        method_namespace = fx.__module__
        # function must be identified in the directory structure matching the domain,
        if not method_namespace.endswith(dotted_identity_domain):
            raise RuntimeError(f'Executor identity does not match location of executor declaration: '
                               f'Identity: {identity}; Declaration location: {method_namespace}')

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
