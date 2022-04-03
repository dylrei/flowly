from ..utils.versioned_identifiers import path_for_identifier


class VersionedDocumentStore(object):
    @classmethod
    def load(cls, identifier, root_path=None):
        with open(path_for_identifier(identifier, root_path), 'r') as document:
            return document.read()
