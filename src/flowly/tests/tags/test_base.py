import yaml

from . import get_test_loader
from ...tags.base import ScalarConfiguredTag, KeywordConfiguredTag, SequenceConfiguredTag, PayloadConfiguredTag, \
    UnconfiguredTag


def _test_tag_configuration(tag_klass, document, expected_value):
    obj = yaml.load(document, Loader=get_test_loader(tag_klass))
    assert obj.__class__.__name__ == tag_klass.tag_name[1:]
    assert obj.value == expected_value


def test_scalar_configured_tag():
    class MyCustomTag(ScalarConfiguredTag):
        tag_name = '!test'

    _test_tag_configuration(
        tag_klass=MyCustomTag,
        document='!test scalar_value',
        expected_value='scalar_value'
    )


def test_keyword_configured_tag():
    class MyCustomTag(KeywordConfiguredTag):
        tag_name = '!testkw'

    snippet = '''
    !testkw
      foo: bar
    '''
    _test_tag_configuration(
        tag_klass=MyCustomTag,
        document=snippet,
        expected_value={'foo': 'bar'}
    )


def test_sequence_configured_tag():
    class MyCustomTag(SequenceConfiguredTag):
        tag_name = '!testseq'

    snippet = '''
    !testseq
      - foo
      - bar
    '''
    _test_tag_configuration(
        tag_klass=MyCustomTag,
        document=snippet,
        expected_value=['foo', 'bar']
    )


def test_payload_configured_tag():
    class MyCustomTag(PayloadConfiguredTag):
        tag_name = '!testpay'

    snippet_as_obj = '''
    !testpay
      foo: bar
    '''
    _test_tag_configuration(
        tag_klass=MyCustomTag,
        document=snippet_as_obj,
        expected_value={'foo': 'bar'}
    )

    snippet_as_seq = '''
    !testpay
      - foo
      - bar
    '''
    _test_tag_configuration(
        tag_klass=MyCustomTag,
        document=snippet_as_seq,
        expected_value=['foo', 'bar']
    )


def test_unconfigured_tag():
    class MyCustomTag(UnconfiguredTag):
        tag_name = '!testnull'
        klass_attributes = {'value': 'arbitrary value'}

    _test_tag_configuration(
        tag_klass=MyCustomTag,
        document='!testnull',
        expected_value='arbitrary value'
    )
