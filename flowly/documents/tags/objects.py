from flowly.constants.tags import TagName
from flowly.documents.tags.base import YAMLConfiguredObject


class MaterialTag(YAMLConfiguredObject):
    tag_name = TagName.Material


class MaterialsTag(YAMLConfiguredObject):
    tag_name = TagName.Materials


class AssetTag(YAMLConfiguredObject):
    tag_name = TagName.Asset


class AssetsTag(YAMLConfiguredObject):
    tag_name = TagName.Assets
