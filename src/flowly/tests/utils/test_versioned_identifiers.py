from ...constants.versioned_document import MetaSectionKey
from ...utils.versioned_identifiers import deconstruct_identifier, construct_identifier, path_for_identifier, \
    identifier_for_path


def test_deconstruct_identifier():
    identifier = 'domain/name::method_name==1.0'
    meta_values = {
        MetaSectionKey.DOMAIN: 'domain/name',
        MetaSectionKey.NAME: 'method_name',
        MetaSectionKey.VERSION: '1.0'
    }
    assert deconstruct_identifier(identifier) == meta_values
    assert construct_identifier(deconstruct_identifier(identifier)) == identifier


def test_construct_identifier():
    identifier = 'domain/name::method_name==1.0'
    meta_values = {
        MetaSectionKey.DOMAIN: 'domain/name',
        MetaSectionKey.NAME: 'method_name',
        MetaSectionKey.VERSION: '1.0'
    }
    assert construct_identifier(meta_values) == identifier
    assert deconstruct_identifier(construct_identifier((meta_values))) == meta_values


def test_path_for_identifier():
    root_path = 'foo/bar'
    identifier = 'domain_org/domain_namespace::method_name==1.0'
    expected_path = 'foo/bar/domain_org/domain_namespace/method_name/1_0.yaml'
    assert path_for_identifier(identifier, root_path=root_path) == expected_path


def test_unimplemented_identifier_for_path():
    try:
        identifier_for_path('whatever')
        run_success = True
    except NotImplementedError as err:
        assert 'Thorny Road to Sadness' in str(err)
        run_success = False
    assert run_success is False
