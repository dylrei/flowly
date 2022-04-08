from yaml import MappingNode, ScalarNode, SequenceNode



def value_unpacker(value):
    from ..tags.base import TagGeneratedObject, TagDescribedData, FlowlyCustomTag
    from ..tags import all_tags
    # todo: use a specification to do this unpacking, then we know what data type to expect
    if isinstance(value, MappingNode):
        return {k.value: value_unpacker(v) for k, v in value.value}
    elif isinstance(value, SequenceNode):
        # import ipdb; ipdb.set_trace()
        return [value_unpacker(v) for v in value.value]
    elif isinstance(value, dict):
        import ipdb; ipdb.set_trace()
        pass
    # if is_mapping(value):
    #     return {k: value_unpacker(v.value) for k, v in value.items()}
    elif isinstance(value, list):
        return list(map(value_unpacker, value))
    elif isinstance(value, FlowlyCustomTag):
        if isinstance(value, TagDescribedData):
            return {value.__class__.__name__: value_unpacker(value.value)}
        elif isinstance(value, TagGeneratedObject):
            # import ipdb; ipdb.set_trace()
            pass
    elif isinstance(value, ScalarNode):
        if hasattr(value, 'tag') and value.tag in all_tags:
            # import ipdb; ipdb.set_trace()
            pass
        return value.value
    elif value in ['true', 'on']:
        return True
    elif value in ['false', 'off']:
        return False
    else:
        return value


def is_mapping(value):
    if isinstance(value, dict):
        return True
    if isinstance(value, MappingNode):
        return True
    # if hasattr(value, '__iter__'):
    #     return {type(item) for item in value} == set([type(('a',))])