from . import run_tag_tests
from ...tags.executor import ActionTag, ValidatorTag, MethodTag


def test_action_tag():
    sample_yaml = '''
    !Action
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        tag_klass=ActionTag,
        document=sample_yaml,
        expected_tag_name='!Action',
        expected_klass_name='Action',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )


def test_method_tag():
    sample_yaml = '''
    !Method
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        tag_klass=MethodTag,
        document=sample_yaml,
        expected_tag_name='!Method',
        expected_klass_name='Method',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )


def test_validator_tag():
    run_tag_tests(
        tag_klass=ValidatorTag,
        document='!Validator validator_identifier',
        expected_tag_name='!Validator',
        expected_klass_name='Validator',
        expected_value='validator_identifier'
    )

