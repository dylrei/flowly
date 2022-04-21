from flowly.constants.identity import IdentityDelimeter
from flowly.constants.names import NamespaceCollection
from flowly.constants.tags import TagName
from flowly.executors.method import YAMLDocument
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
    def executors(self):
        return self._executors

    @property
    def source(self):
        return self._source

    def _resolve_identity(self, identity, collection):
        if IdentityDelimeter.NAMESPACE in identity:
            namespace_name, local_identity = identity.split(IdentityDelimeter.NAMESPACE)
        else:
            namespace_name = self.unique_name
            local_identity = identity
        if namespace_name == self.unique_name:
            if local_identity in getattr(self, collection):
                return getattr(self, collection)[local_identity]
            else:
                raise RuntimeError(f'{identity} does not belong to {collection} collection of namespace {self.unique_name}')
        else:
            if NameStore.exists(namespace_name):
                return NameStore.get_namespace(namespace_name)._resolve_identity(local_identity, collection)
            else:
                raise RuntimeError(f'Unable to resolve namespace {namespace_name} in {identity}')

    def get_method(self, identity):
        from flowly.executors.method import MethodExecutor
        return MethodExecutor(
            identity=identity,
            namespace=self,
            loaded_yaml=self._resolve_identity(identity, NamespaceCollection.METHODS)
        )

    def get_executor(self, identity):
        return self._resolve_identity(identity, NamespaceCollection.EXECUTORS)

    def get_validator(self, identity):
        from flowly.executors.validator import InputValidator
        return InputValidator(
            namespace=self,
            identity=identity,
            loaded_yaml=self._resolve_identity(identity, NamespaceCollection.METHODS)
        )

    def get_specification(self, identity):
        return YAMLDocument(
            identity=identity,
            loaded_yaml=self._resolve_identity(identity, NamespaceCollection.METHODS)
        )

    def register(self, identity, fx):
        self._executors[identity] = fx


    def load_methods(self):
        from ..tags.loader import load_yaml_document
        # Note: because we import descendants before ancestors, any child namespaces are already registered
        for method_path in find_yaml_files(self):
            with open(method_path, 'r') as document:
                method = load_yaml_document(document.read())
                method_identity = construct_identity(method[TagName.META].value)
                self._methods[method_identity] = method


class NameStore(object):
    @classmethod
    def exists(cls, namespace_identity):
        # todo: check if this server is canonical for this namespace
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
