from .base import KeywordConfiguredTag, ScalarConfiguredTag


class ActionTag(KeywordConfiguredTag):
    tag_name = '!Action'


class MethodTag(KeywordConfiguredTag):
    tag_name = '!Method'


class ValidatorTag(ScalarConfiguredTag):
    # the string argument to a validator tag can be either a specification identifier
    # or the name of a registered versioned executor
    tag_name = '!Validator'
