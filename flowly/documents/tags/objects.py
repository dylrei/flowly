from flowly.constants.tags import TagName
from flowly.documents.tags.base import YAMLConfiguredObject


class MaterialTag(YAMLConfiguredObject):
    tag_name = TagName.Material


class AssetTag(YAMLConfiguredObject):
    tag_name = TagName.Asset
