import yaml

from ..constants.method import MethodKeyword


class YAMLConfiguredObject(object):
    control_keys = [MethodKeyword.IDENTITY, MethodKeyword.OUTPUT_TARGET]

    def __init__(self, loader, tag, value):
        self.loader = loader
        self.tag = tag
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def identity(self):
        return self._value[MethodKeyword.IDENTITY]

    @property
    def output_target(self):
        return self._value.get(MethodKeyword.OUTPUT_TARGET)

    @classmethod
    def construct_value(cls, loader, node):
        if isinstance(node, yaml.MappingNode):
            return loader.construct_mapping(node)
        elif isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node)
        elif isinstance(node, yaml.ScalarNode):
            return loader.construct_scalar(node)
        else:
            raise RuntimeError(f'Unexpected node type: {node}')


    def __getitem__(self, item):
        if isinstance(self._value, dict):
            return self._value[item]
        else:
            raise RuntimeError('Attempt to use __getitem__ on tag with an array-shaped value: '
                               '{self.tag} {self.value}')

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if isinstance(self._value, list):
            source = self._value
        else:
            source = sorted(self._value.keys())
        if self.idx + 1 > len(source):
            raise StopIteration
        else:
            output = source[self.idx]
            self.idx += 1
            return output

    def keys(self):
        if isinstance(self.value, dict):
            return self.value.keys()
        else:
            raise RuntimeError('Attempt to use .keys() on tag with an array-shaped value: {self.tag} {self.value}')

    def items(self):
        if isinstance(self.value, dict):
            return self.value.items()
        else:
            raise RuntimeError('Attempt to use .items() on tag with an array-shaped value: {self.tag} {self.value}')


def is_list_of_tuples_mapping(node):
    # mappings are sometimes represented as a list of key:value tuples
    return {type(item) for item in node} == set([type(('a',))])
