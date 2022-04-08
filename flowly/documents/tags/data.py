from .base import YAMLConfiguredObject
from ...constants.tags import TagName


class StateTag(YAMLConfiguredObject):
    tag_name = TagName.State


class InputTag(YAMLConfiguredObject):
    tag_name = TagName.Input
