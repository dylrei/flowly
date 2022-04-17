from ...constants.document import MetaSectionKey
from ...utils.identity import deconstruct_identity, construct_identity


def test_deconstruct_identity():
    identity = 'domain/name::method_name==1.0'
    meta_values = {
        MetaSectionKey.DOMAIN: 'domain/name',
        MetaSectionKey.NAME: 'method_name',
        MetaSectionKey.VERSION: '1.0'
    }
    assert deconstruct_identity(identity) == meta_values
    assert construct_identity(deconstruct_identity(identity)) == identity


def test_construct_identity():
    identity = 'domain/name::method_name==1.0'
    meta_values = {
        MetaSectionKey.DOMAIN: 'domain/name',
        MetaSectionKey.NAME: 'method_name',
        MetaSectionKey.VERSION: '1.0'
    }
    assert construct_identity(meta_values) == identity
    assert deconstruct_identity(construct_identity((meta_values))) == meta_values
