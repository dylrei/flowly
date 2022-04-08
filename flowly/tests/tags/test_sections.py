from . import run_tag_tests
from ...constants.tags import TagName


def test_meta_tag():
    sample_yaml = '''
    !META
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        document=sample_yaml,
        expected_tag_name='!META',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )


def test_body_tag():
    sample_yaml = '''
    !BODY
      - Item One
      - Item Two
      - Item Three'''
    run_tag_tests(
        document=sample_yaml,
        expected_tag_name='!BODY',
        expected_value=['Item One', 'Item Two', 'Item Three']
    )


def test_aliases_tag():
    sample_yaml = '''
    !ALIASES
      - Item One
      - Item Two
      - Item Three'''
    run_tag_tests(
        document=sample_yaml,
        expected_tag_name='!ALIASES',
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
        document=sample_seq_yaml,
        expected_tag_name='!INPUT',
        expected_value=['Item One', 'Item Two', 'Item Three']
    )

    # with object-shaped input
    sample_obj_yaml = '''
    !INPUT
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        document=sample_obj_yaml,
        expected_tag_name='!INPUT',
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
        document=sample_seq_yaml,
        expected_tag_name=TagName.RETURN,
        expected_value=['Item One', 'Item Two', 'Item Three']
    )

    # with object-shaped input
    sample_obj_yaml = '''
    !RETURN
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        document=sample_obj_yaml,
        expected_tag_name='!RETURN',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )
