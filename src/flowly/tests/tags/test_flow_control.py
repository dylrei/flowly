from . import run_tag_tests
from ...tags.flow_control import StepTag


def test_step_tag():
    sample_yaml = '''
    !Step
      kw_one: Value One
      kw_two: Value Two
      kw_three: Value Three'''
    run_tag_tests(
        tag_klass=StepTag,
        document=sample_yaml,
        expected_tag_name='!Step',
        expected_klass_name='Step',
        expected_value={'kw_one': 'Value One', 'kw_two': 'Value Two', 'kw_three': 'Value Three'}
    )