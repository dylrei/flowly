from ..utils.identity import get_dotted_namespace

_executors = {}

class IdentifiedExecutorStore(object):
    @classmethod
    def validate(cls, identity, fx):
        dotted_identity_namespace = get_dotted_namespace(identity),
        method_namespace = fx.__module__
        # function must be identified in the directory/module structure matching the domain/name
        if not method_namespace.endswith(dotted_identity_namespace):
            raise RuntimeError(f'Executor identity does not match location of executor declaration: '
                               f'Identity namespace: {dotted_identity_namespace}; '
                               f'Declaration namespace: {method_namespace}')

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
