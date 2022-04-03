from .. import get_testing_content_root
from ...constants.versioned_document import MetaSectionKey
from ...methods.executor import MethodExecutor
from ...stores.method import MethodStore


def test_method_store():
    root_path = get_testing_content_root()

    identifier_v1 = 'test_cases/document_loading::sample_versioned_method==1.0'
    identifier_v2 = 'test_cases/document_loading::sample_versioned_method==1.1'

    expected_meta_section_v1 = {
        MetaSectionKey.DOCTYPE: 'specification',
        MetaSectionKey.DOMAIN: 'test_cases/document_loading',
        MetaSectionKey.NAME: 'sample_versioned_method',
        MetaSectionKey.VERSION: '1.0',
        MetaSectionKey.STATUS: 'testing'
    }
    expected_meta_section_v2 = dict(expected_meta_section_v1, **{MetaSectionKey.VERSION: '1.1'})

    # load version 1.0
    obj = MethodStore.load(identifier_v1, root_path)
    assert isinstance(obj, MethodExecutor) is True
    assert obj.identifier == identifier_v1
    assert obj.meta_section == expected_meta_section_v1
    assert obj.meta_section[MetaSectionKey.VERSION] == '1.0'

    # load version 1.1
    obj = MethodStore.load(identifier_v2, root_path)
    assert isinstance(obj, MethodExecutor) is True
    assert obj.identifier == identifier_v2
    assert obj.meta_section == expected_meta_section_v2
    assert obj.meta_section[MetaSectionKey.VERSION] == '1.1'
