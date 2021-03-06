from .base import YAMLConfiguredObject
from ..constants.tags import TagName


class MetaTag(YAMLConfiguredObject):
    tag_name = TagName.META

    @classmethod
    def construct_value(cls, loader, node):
        # meta section values are *always* strings, even if they *could* be represented as a float or int
        value = super(MetaTag, cls).construct_value(loader, node)
        return {k: str(v) for k, v in value.items()}
