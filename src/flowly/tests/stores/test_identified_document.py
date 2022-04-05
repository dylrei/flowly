from ...stores.identified_document import IdentifiedDocumentStore


def test_identified_document_store():
    identity1 = 'test_cases/document_loading::sample_versioned_document==1.0'
    identity2 = 'test_cases/document_loading::sample_versioned_document==1.1'
    assert IdentifiedDocumentStore.use(identity1) == 'success: true'
    assert IdentifiedDocumentStore.use(identity2) == 'success: totes'
