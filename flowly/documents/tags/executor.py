from .base import YAMLConfiguredObject
from ...constants.tags import TagName


class ActionTag(YAMLConfiguredObject):
    tag_name = TagName.Action


class MethodTag(YAMLConfiguredObject):
    tag_name = TagName.Method


class ValidatorTag(YAMLConfiguredObject):
    tag_name = TagName.Validator
