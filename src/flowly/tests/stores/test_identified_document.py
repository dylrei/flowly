from ...constants.context import DocumentLoaderContext
from ...stores.identified_document import IdentifiedDocumentStore
from ...tags.loader import load_yaml_document


def test_identified_document_store():
    identity = 'test_cases/document_loading::sample_versioned_document==1.0'
    expected = {
        'MetaSection': {
            'domain': 'test_cases/document_loading',
            'method': 'sample_versioned_document',
            'version': '1.0',
            'status': 'development'
        }
    }
    assert load_yaml_document(IdentifiedDocumentStore.use(identity), DocumentLoaderContext.SPECIFICATION) == expected

    identity = 'test_cases/document_loading::sample_versioned_document==1.1'
    expected = {
        'MetaSection': {
            'domain': 'test_cases/document_loading',
            'method': 'sample_versioned_document',
            'version': '1.1',
            'status': 'development'
        }
    }
    assert load_yaml_document(IdentifiedDocumentStore.use(identity), DocumentLoaderContext.SPECIFICATION) == expected
