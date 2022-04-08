import yaml

from .tags import get_klass_for_tag

_loader = yaml.SafeLoader


def _object_constructor(loader, node):
    klass = get_klass_for_tag(node.tag)
    return klass(loader, node.tag, node.value)

# tag value of None means "for all unmatched tags"
_loader.add_constructor(None, _object_constructor)


def _load_yaml(document):
    # for testing, mostly
    return yaml.load(document, Loader=_loader)


def load_yaml_document(document):
    return {
        node.tag: node
        for node in _load_yaml(document)
    }