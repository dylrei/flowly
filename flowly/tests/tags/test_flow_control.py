from . import run_tag_tests


def test_step_tag():
    sample_yaml = '''
    !Step
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        document=sample_yaml,
        expected_tag_name='!Step',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )