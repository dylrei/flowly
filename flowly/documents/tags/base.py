import yaml


class YAMLConfiguredObject(object):
    def __init__(self, loader, tag, value):
        self.loader = loader
        self.tag = tag
        self.value = value  #self.construct_value(node)

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


class YAMLConfiguredNode(YAMLConfiguredObject):
    def __getitem__(self, item):
        if isinstance(self.value, dict):
            return self.value[item]
        else:
            raise RuntimeError('Attempt to use __getitem__ on an array-shaped tag object: {self.tag} {self.value}')

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):

        if isinstance(self.value, list):
            source = self.value
        else:
            source = sorted(self.value.keys())
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
            raise RuntimeError('Attempt to use .keys() on an array-shaped tag object: {self.tag} {self.value}')

    def items(self):
        if isinstance(self.value, dict):
            return self.value.items()
        else:
            raise RuntimeError('Attempt to use .items() on an array-shaped tag object: {self.tag} {self.value}')


def is_list_of_tuples_mapping(node):
    # mappings are sometimes represented as a list of key:value tuples
    return {type(item) for item in node} == set([type(('a',))])
