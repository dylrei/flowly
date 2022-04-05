from ...constants.identity import MetaSectionKey
from ...utils.identity import deconstruct_identity, construct_identity, path_for_identity, \
    identity_for_path


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


def _test_path_for_identity():
    root_path = 'foo/bar'
    identity = 'domain_org/domain_namespace::method_name==1.0'
    expected_path = 'foo/bar/domain_org/domain_namespace/method_name/1_0.yaml'
    assert path_for_identity(identity, root_path=root_path) == expected_path


def test_unimplemented_identity_for_path():
    try:
        identity_for_path('whatever')
        run_success = True
    except NotImplementedError as err:
        assert 'Thorny Road to Sadness' in str(err)
        run_success = False
    assert run_success is False
