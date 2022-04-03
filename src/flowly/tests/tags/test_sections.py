from . import run_tag_tests
from ...tags.sections import MetaSectionTag, BodySectionTag, AliasesSectionTag, InputSectionTag, ReturnSectionTag


def test_meta_tag():
    sample_yaml = '''
    !META
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        tag_klass=MetaSectionTag,
        document=sample_yaml,
        expected_tag_name='!META',
        expected_klass_name='MetaSection',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )


def test_body_tag():
    sample_yaml = '''
    !BODY
      - Item One
      - Item Two
      - Item Three'''
    run_tag_tests(
        tag_klass=BodySectionTag,
        document=sample_yaml,
        expected_tag_name='!BODY',
        expected_klass_name='BodySection',
        expected_value=['Item One', 'Item Two', 'Item Three']
    )


def test_aliases_tag():
    sample_yaml = '''
    !ALIASES
      - Item One
      - Item Two
      - Item Three'''
    run_tag_tests(
        tag_klass=AliasesSectionTag,
        document=sample_yaml,
        expected_tag_name='!ALIASES',
        expected_klass_name='AliasesSection',
        expected_value=['Item One', 'Item Two', 'Item Three']
    )


def test_input_tag():
    # with sequence-shaped input
    sample_seq_yaml = '''
    !INPUT
      - Item One
      - Item Two
      - Item Three'''
    run_tag_tests(
        tag_klass=InputSectionTag,
        document=sample_seq_yaml,
        expected_tag_name='!INPUT',
        expected_klass_name='InputSection',
        expected_value=['Item One', 'Item Two', 'Item Three']
    )

    # with object-shaped input
    sample_obj_yaml = '''
    !INPUT
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        tag_klass=InputSectionTag,
        document=sample_obj_yaml,
        expected_tag_name='!INPUT',
        expected_klass_name='InputSection',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )



def test_return_tag():
    # with sequence-shaped input
    sample_seq_yaml = '''
    !RETURN
      - Item One
      - Item Two
      - Item Three'''
    run_tag_tests(
        tag_klass=ReturnSectionTag,
        document=sample_seq_yaml,
        expected_tag_name='!RETURN',
        expected_klass_name='ReturnSection',
        expected_value=['Item One', 'Item Two', 'Item Three']
    )

    # with object-shaped input
    sample_obj_yaml = '''
    !RETURN
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        tag_klass=ReturnSectionTag,
        document=sample_obj_yaml,
        expected_tag_name='!RETURN',
        expected_klass_name='ReturnSection',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )
