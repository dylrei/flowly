class ScalarConfiguredObject(object):
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value


class KeywordConfiguredObject(object):
    def __init__(self, tag, value):
        self.tag = tag
        self.value = {k.value: v.value for k, v in value}


class SequenceConfiguredObject(object):
    def __init__(self, tag, value):
        self.tag = tag
        self.value = [item.value for item in value]


class UnconfiguredObject(object):
    def __init__(self, tag, *args, **kwargs):
        # value is set via klass_attributes
        self.tag = tag


class CustomYamlTag(object):
    tag_name = None
    klass = None
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
        klass_name = cls.tag_name[1:]
        base_klass = cls._get_base_klass(node.value)
        klass = type(klass_name, (base_klass, *mixin_klasses), klass_attributes)
        return klass(tag=cls.tag_name, value=node.value)

    @classmethod
    def representer(self):
        raise NotImplementedError('TBD')


class ScalarConfiguredTag(CustomYamlTag):
    base_klass = ScalarConfiguredObject
    constrain_values = None

    @classmethod
    def _validate(cls, value):
        if cls.constrain_values is not None:
            if value not in cls.constrain_values:
                raise RuntimeError(f'Invalid value for {cls.tag_name} tag: {value}')


class KeywordConfiguredTag(CustomYamlTag):
    base_klass = KeywordConfiguredObject


class SequenceConfiguredTag(CustomYamlTag):
    base_klass = SequenceConfiguredObject


class PayloadConfiguredTag(CustomYamlTag):
    # a payload root node may be either array-shaped or object-shaped
    @classmethod
    def _get_base_klass(cls, value):
        # is this a list of scalars or a list of key-value tuples?
        if {type(item) for item in value} == set([type(('a',))]):
            return KeywordConfiguredObject
        else:
            return SequenceConfiguredObject


class UnconfiguredTag(CustomYamlTag):
    base_klass = UnconfiguredObject
