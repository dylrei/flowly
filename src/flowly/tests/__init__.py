from ..namespacing.root import ContentRoot

# package tests may only interact with content in or below the tests/ directory
ContentRoot(__name__)

def import_target():
    pass
