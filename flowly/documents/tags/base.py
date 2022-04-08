import yaml


class YAMLConfiguredObject(object):
    def __init__(self, loader, tag, node):
        self.loader = loader
        self.tag = tag
        self.value = self.construct_value(node)

    def construct_value(self, node):
        from ..loader import _object_constructor
        if hasattr(node, 'tag') and not node.tag.startswith('tag:yaml.org'):
            return _object_constructor(self.loader, node)
        if isinstance(node, yaml.nodes.ScalarNode):
            return self.loader.construct_scalar(node)
        elif isinstance(node, yaml.nodes.SequenceNode):
            return self.loader.construct_sequence(node)
        elif isinstance(node, yaml.nodes.MappingNode):
            return self.loader.construct_mapping(node)
        if is_list_of_tuples_mapping(node):
            return {self.construct_value(k): self.construct_value(v) for k, v in node}
        elif isinstance(node, list):
            return [self.construct_value(i) for i in node]
        elif isinstance(node, str):
            return node
        raise RuntimeError(f'Unable to construct node: {node}')


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
