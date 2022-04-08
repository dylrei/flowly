from . import run_tag_tests
from ...constants.tags import TagName
from ...documents.loader import _load_yaml


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
      id: validator_identity
      favorite_number:
        data_type: int
    '''
    run_tag_tests(
        document=sample_yaml,
        expected_tag_name='!Validator',
        expected_value={'id': 'validator_identity', 'favorite_number': {'data_type': 'int'}}
    )


def test_run_action():
    sample_yaml = '''
    - !Action
      id: core/math::subtract==production
      left: 27.0
      right: 11
      store_return: !State my_return
'''
    loaded_doc = _load_yaml(sample_yaml)
    action = loaded_doc[0]
    assert action.execute() == {TagName.State: {'my_return': 16}}
    assert action.return_value == 16


def test_run_validator():
    sample_yaml = '''
    - !Validator
      id: specifications/testing::simple_yaml_spec==1.0
    '''
    sample_data = {
        'name': 'Will Riker',
        'favorite_number': 1
    }
    loaded_doc = _load_yaml(sample_yaml)
    validator = loaded_doc[0]
    assert validator.validate(sample_data) is True
