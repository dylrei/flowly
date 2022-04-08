from . import run_tag_tests


def test_action_tag():
    sample_yaml = '''
    !Action
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        document=sample_yaml,
        expected_tag_name='!Action',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )


def test_method_tag():
    sample_yaml = '''
    !Method
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        document=sample_yaml,
        expected_tag_name='!Method',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )


def test_validator_tag():
    sample_yaml = '''
    !Validator
      id: validator_identity'''
    run_tag_tests(
        document=sample_yaml,
        expected_tag_name='!Validator',
        expected_value={'id': 'validator_identity'}
    )

