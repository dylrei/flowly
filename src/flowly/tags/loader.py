import yaml

from .base import value_unpacker
from .executor import ActionTag, ValidatorTag, MethodTag
from .flow_control import StepTag
from .objects import MaterialTag, AssetTag, DataTag
from .sections import MetaSectionTag, InputSectionTag, BodySectionTag, ReturnSectionTag, AliasesSectionTag
from ..constants.context import DocumentLoaderContext
from ..constants.document import DocumentSectionName

method_tag_klasses = [
    # sections
    MetaSectionTag, InputSectionTag, BodySectionTag, ReturnSectionTag, AliasesSectionTag,

    # objects
    MaterialTag, AssetTag, DataTag,

    # executors
    ActionTag, ValidatorTag, MethodTag,

    # flow control
    StepTag,
]

# validation mode: use of non-validation executors and tags is not supported
specification_tag_klasses = [MetaSectionTag, InputSectionTag, MaterialTag]

klasses_for_context = {
    DocumentLoaderContext.SPECIFICATION: specification_tag_klasses,
    DocumentLoaderContext.METHOD: method_tag_klasses
}


def get_loader(context):
    loader = yaml.SafeLoader
    for klass in klasses_for_context[context]:
        loader.add_constructor(klass.tag_name, klass.constructor)
    return loader


def load_yaml_document(document, context):
    return {
        node.__class__.__name__: value_unpacker(node)
        for node in yaml.load(document, Loader=get_loader(context))
        if node.__class__.__name__ != DocumentSectionName.ALIASES
    }
