from flowly.constants.identity import IdentityDelimeter
from flowly.constants.tags import TagName
from flowly.utils.identity import construct_identity
from flowly.utils.names import find_yaml_files

_names = dict()

class Namespace(object):
    def __init__(self, unique_name, file_path, canonical, source):
        self._unique_name = unique_name
        self._path = '/'.join(file_path.split('/')[:-1])
        self._canonical = canonical
        self._source = source
        self._methods = dict()
        self._executors = dict()
        self.load_methods()

    @property
    def unique_name(self):
        return self._unique_name

    @property
    def path(self):
        return self._path

    @property
    def canonical(self):
        return self._canonical

    @property
    def methods(self):
        return self._methods

    @property
    def source(self):
        return self._source

    def get_method(self, identity):
        from flowly.executors.method import MethodExecutor
        if identity not in self.methods:
            raise RuntimeError(f'Method {identity} not found in Namespace {self.unique_name}')
        return MethodExecutor(
            identity=identity,
            namespace=self,
            loaded_yaml=self.methods[identity]
        )
        # return self.methods[identity]

    def get_executor(self, identity):
        if identity not in self._executors:
            # does this belong to a different namespace?
            if IdentityDelimeter.NAMESPACE in identity:
                namespace_identity, local_identity = identity.split(IdentityDelimeter.NAMESPACE)
                if NameStore.exists(namespace_identity):
                    return NameStore.get_namespace(namespace_identity).get_executor(local_identity)
            import ipdb; ipdb.set_trace()
        return self._executors[identity]

    def is_namespace(self, path):
        pass

    def register(self, identity, fx):
        self._executors[identity] = fx


    def load_methods(self):
        from flowly.documents.loader import load_yaml_document
        # Note: because we import descendants before ancestors, any child namespaces are already registered
        for method_path in find_yaml_files(self):
            with open(method_path, 'r') as document:
                method = load_yaml_document(document.read())
                print(method, method_path)
                method_identity = construct_identity(method[TagName.META].value)
                self._methods[method_identity] = method


class NameStore(object):
    @classmethod
    def exists(cls, namespace_identity):
        return namespace_identity in _names


    @classmethod
    def register(cls, unique_name, file_path, canonical, source):
        global _names
        if unique_name in _names:
            raise RuntimeError(f'Namespace collision: {unique_name}; First registration from: '
                               f'{_names[unique_name].file_path}; Second registration from: {file_path}')
        else:
            _names[unique_name] = Namespace(
                unique_name=unique_name,
                file_path=file_path,
                canonical=canonical,
                source=source
            )
            return _names[unique_name]

    @classmethod
    def get_namespace(cls, ns_identity):
        if cls.exists(ns_identity):
            return _names[ns_identity]
