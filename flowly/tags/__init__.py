from .base import YAMLConfiguredObject
from .executor import ValidatorTag, MethodTag, ActionTag, StepTag
from .objects import AssetTag, MaterialTag
from .section import MetaTag

_special_tag_klasses = [ActionTag, MethodTag, ValidatorTag, MaterialTag, AssetTag, MetaTag, StepTag]
_default_klass = YAMLConfiguredObject

_klass_by_tag = {klass.tag_name: klass for klass in _special_tag_klasses}

def get_klass_for_tag(tag):
    return _klass_by_tag.get(tag, _default_klass)
