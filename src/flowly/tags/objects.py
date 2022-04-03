from .base import ScalarConfiguredTag


class MaterialTag(ScalarConfiguredTag):
    tag_name = '!Material'


class AssetTag(ScalarConfiguredTag):
    tag_name = '!Asset'


class DataTag(ScalarConfiguredTag):
    tag_name = '!Data'
