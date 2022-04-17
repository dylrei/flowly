from constant_namespace import ConstantNamespace


class MetaSectionKey(ConstantNamespace):
    DOCTYPE = 'doctype'
    DOMAIN = 'domain'
    NAME = 'name'
    VERSION = 'version'
    STATUS = 'status'


class IdentityDelimeter(ConstantNamespace):
    NAMESPACE = '++'
    DOMAIN = '::'
    VERSION = '=='
