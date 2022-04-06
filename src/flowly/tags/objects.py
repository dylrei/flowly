from .base import ObjectTag


class MaterialTag(ObjectTag):
    tag_name = '!Material'


class AssetTag(ObjectTag):
    tag_name = '!Asset'


class DataTag(ObjectTag):
    tag_name = '!Data'
