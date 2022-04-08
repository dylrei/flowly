from ...constants.context import DocumentLoaderContext
from ...constants.tags import TagName
from ...stores.identified_document import IdentifiedDocumentStore
from ...documents.loader import load_yaml_document


def test_identified_document_store():
    identity = 'test_cases/document_loading::sample_versioned_document==1.0'
    expected = {
        'domain': 'test_cases/document_loading',
        'method': 'sample_versioned_document',
        'version': '1.0',
        'status': 'development'
    }
    assert load_yaml_document(IdentifiedDocumentStore.use(identity))[TagName.META].value == expected

    identity = 'test_cases/document_loading::sample_versioned_document==1.1'
    expected = {
        'domain': 'test_cases/document_loading',
        'method': 'sample_versioned_document',
        'version': '1.1',
        'status': 'development'
    }
    assert load_yaml_document(IdentifiedDocumentStore.use(identity))[TagName.META].value == expected
