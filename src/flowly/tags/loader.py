import yaml

from .executor import ActionTag, ValidatorTag, MethodTag
from .flow_control import StepTag
from .objects import MaterialTag, AssetTag, DataTag
from .sections import MetaSectionTag, InputSectionTag, BodySectionTag, ReturnSectionTag, AliasesSectionTag
from ..constants.tags import MethodSectionName


tag_klasses = [
    # sections
    MetaSectionTag, InputSectionTag, BodySectionTag, ReturnSectionTag, AliasesSectionTag,
    # objects
    MaterialTag, AssetTag, DataTag,
    # executors
    ActionTag, ValidatorTag, MethodTag,
    # flow control
    StepTag,
]


def get_loader():
    loader = yaml.SafeLoader
    for klass in tag_klasses:
        loader.add_constructor(klass.tag_name, klass.constructor)
    return loader


def load_yaml(document):
    return {
        node.__class__.__name__: node
        for node in yaml.load(document, Loader=get_loader())
        if node.__class__.__name__ != MethodSectionName.ALIASES
    }
