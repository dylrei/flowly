from .base import ObjectTag


class ExecutorObjectMixin(object):
    permitted_callables = None


class ActionTag(ObjectTag):
    tag_name = '!Action'
    mixin_klasses = [ExecutorObjectMixin]


class MethodTag(ObjectTag):
    tag_name = '!Method'
    mixin_klasses = [ExecutorObjectMixin]


class ValidatorTag(ObjectTag):
    tag_name = '!Validator'
    mixin_klasses = [ExecutorObjectMixin]
