from .base import SequenceConfiguredTag, PayloadConfiguredTag, KeywordConfiguredTag


class Section(object):
    def __init__(self, tag, value):
        self.tag = tag
        self.contents = value

# Keyword-configured tags
# =========================
class MetaSectionTag(KeywordConfiguredTag):
    tag_name = '!META'
    klass_name = 'MetaSection'


# Sequence-configured tags
# =========================
class BodySectionTag(SequenceConfiguredTag):
    tag_name = '!BODY'
    klass_name = 'BodySection'


class AliasesSectionTag(SequenceConfiguredTag):
    tag_name = '!ALIASES'
    klass_name = 'AliasesSection'


# Payload-configured tags
# =========================
class InputSectionTag(PayloadConfiguredTag):
    tag_name = '!INPUT'
    klass_name = 'InputSection'


class ReturnSectionTag(PayloadConfiguredTag):
    tag_name = '!RETURN'
    klass_name = 'ReturnSection'
