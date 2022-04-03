from constant_namespace import ConstantNamespace


class MetaSectionKey(ConstantNamespace):
    DOMAIN = 'domain'
    NAME = 'name'
    VERSION = 'version'


class IdentifierDelimeter(ConstantNamespace):
    DOMAIN = '::'
    VERSION = '=='
