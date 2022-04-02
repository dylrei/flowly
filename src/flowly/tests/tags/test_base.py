import yaml

from ...tags.base import ScalarConfiguredTag, KeywordConfiguredTag, SequenceConfiguredTag, PayloadConfiguredTag, \
    UnconfiguredTag


def _test_tag_configuration(tag_klass, document, expected_value):
    loader = yaml.SafeLoader
    loader.add_constructor(tag_klass.tag_name, tag_klass.constructor)
    obj = yaml.load(document, Loader=loader)
    assert obj.value == expected_value


def test_scalar_configured_tag():
    class MyCustomTag(ScalarConfiguredTag):
        tag_name = '!test'

    snippet = '!test scalar_value'
    expected_value = 'scalar_value'
    _test_tag_configuration(MyCustomTag, snippet, expected_value)


def test_keyword_configured_tag():
    class MyCustomTag(KeywordConfiguredTag):
        tag_name = '!testkw'

    snippet = '''
    !testkw
      foo: bar
    '''
    expected_value = {'foo': 'bar'}
    _test_tag_configuration(MyCustomTag, snippet, expected_value)


def test_sequence_configured_tag():
    class MyCustomTag(SequenceConfiguredTag):
        tag_name = '!testseq'

    snippet = '''
    !testseq
      - foo
      - bar
    '''
    expected_value = ['foo', 'bar']
    _test_tag_configuration(MyCustomTag, snippet, expected_value)


def test_payload_configured_tag():
    class MyCustomTag(PayloadConfiguredTag):
        tag_name = '!testpay'

    snippet_as_obj = '''
    !testpay
      foo: bar
    '''
    expected_obj_value = {'foo': 'bar'}
    _test_tag_configuration(MyCustomTag, snippet_as_obj, expected_obj_value)

    snippet_as_seq = '''
    !testpay
      - foo
      - bar
    '''
    expected_seq_value = ['foo', 'bar']
    _test_tag_configuration(MyCustomTag, snippet_as_seq, expected_seq_value)


def test_unconfigured_tag():
    class MyCustomTag(UnconfiguredTag):
        tag_name = '!testnull'
        klass_attributes = {'value': 'arbitrary value'}

    snippet = '!testnull'
    expected_value = 'arbitrary value'
    _test_tag_configuration(MyCustomTag, snippet, expected_value)
