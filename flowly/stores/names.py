from collections import defaultdict

from flowly.constants.identity import IdentityDelimeter
from flowly.constants.tags import TagName
from flowly.utils.identity import construct_identity
from flowly.utils.names import find_yaml_files

_names = dict()
_models = defaultdict(list)

class Namespace(object):
    def __init__(self, unique_name, file_path, canonical, source):
        self._unique_name = unique_name
        self._path = '/'.join(file_path.split('/')[:-1])
        self._canonical = canonical
        self._source = source
        self._methods = dict()
        self._executors = dict()
        self._models = dict()
        self.load_methods()
        self.load_models()

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

    def get_executor(self, identity):
        if identity not in self._executors:
            # does this belong to a different namespace?
            if IdentityDelimeter.NAMESPACE in identity:
                namespace_identity, local_identity = identity.split(IdentityDelimeter.NAMESPACE)
                if NameStore.exists(namespace_identity):
                    return NameStore.get_namespace(namespace_identity).get_executor(local_identity)
            raise RuntimeError(f'Executor {identity} not registered in Namespace {self.unique_name}. Is the '
                               f'containing module imported in the {self.unique_name} __init__.py file?')
        return self._executors[identity]

    def get_validator(self, identity):
        from flowly.executors.validator import InputValidator
        if identity not in self.methods:
            raise RuntimeError(f'Validator {identity} not found in Namespace {self.unique_name}')
        return InputValidator(
            identity=identity,
            namespace=self,
            loaded_yaml=self.methods[identity]
        )

    def is_namespace(self, path):
        pass

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

    def load_models(self):
        # we load this way because Django models will load before our namespaces, thus the need to
        # defer loading until the namespace actually exists
        for model in _models[self.unique_name]:
            model.namespace = self
            self._models[model.barcode_prefix] = model
        # material models should only be accessed via the namespace
        del _models[self.unique_name]

    def _load_object(self, identity):
        barcode = identity.split(IdentityDelimeter.NAMESPACE)[-1]
        for barcode_prefix, model in self._models.items():
            if barcode.startswith(barcode_prefix):
                try:
                    return model.objects.get(**{model.barcode_field_name: barcode})
                except model.DoesNotExist:
                    import ipdb; ipdb.set_trace()
                    raise RuntimeError(f'adf')
        raise RuntimeError(f'Unable to load Material {identity}: no model for barcode prefix {barcode_prefix}')

    def load_one_material(self, identity):
        if isinstance(identity, list):
            raise RuntimeError(f'Attempt to use !Material to load array of identities: {identity}')
        return self._load_object(identity)

    def load_one_asset(self, identity):
        if isinstance(identity, list):
            raise RuntimeError(f'Attempt to use !Asset to load array of identities: {identity}')
        # todo: load object in a read-only way
        return self._load_object(identity)

    def load_many_materials(self, identities):
        if isinstance(identities, str):
            raise RuntimeError(f'Attempt to use !Materials to load single identity: {identities}')
        return [self._load_object(identity) for identity in identities]

    def load_many_assets(self, identities):
        if isinstance(identities, str):
            raise RuntimeError(f'Attempt to use !Assets to load single identity: {identities}')
        # todo: load objects in a read-only way
        return [self._load_object(identity) for identity in identities]




class NameStore(object):
    @classmethod
    def exists(cls, namespace_identity):
        return namespace_identity in _names


    @classmethod
    def register(cls, unique_name, file_path, canonical, source):
        global _names
        if file_path.endswith('/__init__.py'):
            file_path = file_path[:-len('/__init__.py')]

        if unique_name in _names:
            return _names[unique_name]
        else:
            _names[unique_name] = Namespace(
                unique_name=unique_name,
                file_path=file_path,
                canonical=canonical,
                source=source
            )
            return _names[unique_name]

    @classmethod
    def register_model(cls, namespace_identity, model):
        global _models
        _models[namespace_identity].append(model)

    @classmethod
    def get_namespace(cls, ns_identity):
        if cls.exists(ns_identity):
            return _names[ns_identity]
