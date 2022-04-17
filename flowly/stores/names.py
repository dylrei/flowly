from flowly.constants.document import MetaSectionKey
from flowly.utils.identity import deconstruct_identity

_names = dict()

class Namespace(object):
    def __init__(self, unique_name, file_path, module_path, canonical, source, actions, namespaces):
        self._unique_name = unique_name
        self._file_path = '/'.join(file_path.split('/')[:-1])
        self._module_path = module_path
        self._canonical = canonical
        self._source = source
        self._actions = actions
        self._namespaces = namespaces

    @property
    def unique_name(self):
        return self._unique_name

    @property
    def file_path(self):
        return self._file_path

    @property
    def module_path(self):
        return self._module_path

    @property
    def canonical(self):
        return self._canonical

    @property
    def source(self):
        return self._source

    @property
    def actions(self):
        return self._actions

    @property
    def namespaces(self):
        return self._namespaces


class NameStore(object):
    @classmethod
    def register(cls, unique_name, file_path, module_path, canonical, source, actions, namespaces):
        global _names
        if unique_name in _names:
            raise RuntimeError(f'Namespace collision: {unique_name}; First registration from: '
                               f'{_names[unique_name].file_path}; Second registration from: {file_path}')
        else:
            # will we need to do something to "load" our actions? import all, likely?
            _names[unique_name] = Namespace(
                unique_name=unique_name,
                file_path=file_path,
                module_path=module_path,
                canonical=canonical,
                source=source,
                actions=actions,
                namespaces=namespaces
            )
            return _names[unique_name]

    @classmethod
    def get_namespace(cls, identity):
        return _names[deconstruct_identity(identity)[MetaSectionKey.DOMAIN].split('/')[0]]
