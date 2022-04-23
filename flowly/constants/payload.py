from constant_namespace import ConstantNamespace


class PayloadKey(ConstantNamespace):
    REQUEST = 'request'
    DATA = 'data'
    NEXT = 'next'
    METHOD = 'method'
    STATE = 'state'
    NAMESPACE = 'namespace'
    TIMESTAMP = 'timestamp'
    COMPLETED = 'completed'
    DUPLICATE = 'duplicate'
