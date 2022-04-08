from ...constants.document import MetaSectionKey, DocumentStatus
from ...executors.method import MethodExecutor
from ...stores.method import MethodStore


def test_method_store():
    identifier_v1 = 'test_cases/document_loading::sample_versioned_method==1.0'
    identifier_v2 = 'test_cases/document_loading::sample_versioned_method==1.1'

    expected_meta_section_v1 = {
        MetaSectionKey.DOMAIN: 'test_cases/document_loading',
        MetaSectionKey.NAME: 'sample_versioned_method',
        # version is always a string, even if it *could* be represented as a float/int
        MetaSectionKey.VERSION: '1.0',
        MetaSectionKey.STATUS: DocumentStatus.TESTING,
    }
    expected_meta_section_v2 = dict(expected_meta_section_v1, **{MetaSectionKey.VERSION: '1.1'})

    # load version 1.0
    obj = MethodStore.load(identifier_v1)
    assert isinstance(obj, MethodExecutor) is True
    assert obj.identity == identifier_v1
    assert obj.meta_section == expected_meta_section_v1
    assert obj.meta_section[MetaSectionKey.VERSION] == '1.0'

    # load version 1.1
    obj = MethodStore.load(identifier_v2)
    assert isinstance(obj, MethodExecutor) is True
    assert obj.identity == identifier_v2
    assert obj.meta_section == expected_meta_section_v2
    assert obj.meta_section[MetaSectionKey.VERSION] == '1.1'
