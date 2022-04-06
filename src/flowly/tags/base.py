def value_unpacker(value):
    if is_mapping(value):
        if isinstance(value, list):
            # a list of key-value tuples
            return {k.value: value_unpacker(v.value) for k, v in value}
        return {k: value_unpacker(v.value) for k, v in value.items()}
    elif isinstance(value, list):
        return [value_unpacker(v.value) for v in value]
    elif hasattr(value, 'value'):
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
    if hasattr(value, '__iter__'):
        return {type(item) for item in value} == set([type(('a',))])


class TagGeneratedObject(object):
    def __init__(self, tag, node):
        self.tag = tag
        # not exposing a public "value" attribute prevents further recursive yaml processing, leaving this object
        # in place of the node
        self._value = value_unpacker(node.value)


class TagDescribedData(object):
    def __init__(self, tag, node):
        self.tag = tag
        # setting self.value means that yaml loading will treat this object like an array or object data structure,
        # a name we gave to a collection of other values
        self.value = value_unpacker(node.value)


class CustomYamlTag(object):
    tag_name = None
    klass = None
    klass_name = None
    base_klass = None
    mixin_klasses = None
    klass_attributes = None

    @classmethod
    def _validate(cls, value):
        pass

    @classmethod
    def _get_base_klass(cls, value):
        return cls.base_klass

    @classmethod
    def constructor(cls, loader, node):
        cls._validate(node.value)
        mixin_klasses = cls.mixin_klasses or tuple()
        klass_attributes = cls.klass_attributes or dict()
        klass_name = cls.klass_name or cls.tag_name[1:]
        base_klass = cls._get_base_klass(node.value)
        klass = type(klass_name, (base_klass, *mixin_klasses), klass_attributes)
        return klass(tag=cls.tag_name, node=node)

    @classmethod
    def representer(self):
        raise NotImplementedError('TBD')


class LabelTag(CustomYamlTag):
    base_klass = TagDescribedData

class ObjectTag(CustomYamlTag):
    base_klass = TagGeneratedObject
