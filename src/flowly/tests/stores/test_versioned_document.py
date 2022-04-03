from ... import get_testing_content_root
from ...stores.versioned_document import VersionedDocumentStore


def test_versioned_document_store():
    root_path = get_testing_content_root()
    identifier = 'test_cases/document_loading::sample_versioned_document==1.0'
    document_content = VersionedDocumentStore.load(identifier, root_path=root_path)
    assert document_content == 'success: true'
