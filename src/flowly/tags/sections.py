from .base import LabelTag


# Keyword-configured tags
# =========================
class MetaSectionTag(LabelTag):
    tag_name = '!META'
    klass_name = 'MetaSection'


# Sequence-configured tags
# =========================
class BodySectionTag(LabelTag):
    tag_name = '!BODY'
    klass_name = 'BodySection'


class AliasesSectionTag(LabelTag):
    tag_name = '!ALIASES'
    klass_name = 'AliasesSection'


# Payload-configured tags
# =========================
class InputSectionTag(LabelTag):
    tag_name = '!INPUT'
    klass_name = 'InputSection'


class ReturnSectionTag(LabelTag):
    tag_name = '!RETURN'
    klass_name = 'ReturnSection'
