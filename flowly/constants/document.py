from constant_namespace import ConstantNamespace


class YamlKeyword(ConstantNamespace):
    DATA_TYPE = 'data_type'
    REQUIRED = 'required'
    MIN_SIZE = 'min_size'
    MAX_SIZE = 'max_size'
    MEMBER_DATA_TYPE = 'member_data_type'
    MEMBER_SPEC = 'member_spec'
    VALIDATOR = 'validator'


class MetaSectionKey(ConstantNamespace):
    DOMAIN = 'domain'
    NAME = 'name'
    VERSION = 'version'
    STATUS = 'status'


class DocumentStatus(ConstantNamespace):
    PRODUCTION = 'production'
    TESTING = 'testing'
    DEVELOPMENT = 'development'


class DataType(ConstantNamespace):
    STRING = 'string'
    INTEGER = 'integer'
    FLOAT = 'float'
    BOOLEAN = 'boolean'
    OBJECT = 'object'
    ARRAY = 'array'
    MATERIAL = 'material'
    NODE = 'node'


class DocumentSectionName(ConstantNamespace):
    META = 'MetaSection'
    ALIASES = 'AliasesSection'
    INPUT = 'InputSection'
    BODY = 'BodySection'
    RETURN = 'ReturnSection'
