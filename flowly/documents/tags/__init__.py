from .base import YAMLConfiguredNode
from .executor import ValidatorTag, MethodTag, ActionTag
from .objects import AssetTag, MaterialTag

_special_tag_klasses = [ActionTag, MethodTag, ValidatorTag, MaterialTag, AssetTag]
_default_klass = YAMLConfiguredNode

_klass_by_tag = {klass.tag_name: klass for klass in _special_tag_klasses}

def get_klass_for_tag(tag):
    klass = _klass_by_tag.get(tag, _default_klass)
    return klass
