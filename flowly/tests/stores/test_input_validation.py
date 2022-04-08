from ...stores.input_validation import InputValidatorStore


def test_input_validator_store():
    identity = 'specifications/testing::simple_yaml_spec==1.0'
    validator = InputValidatorStore.get_validator(identity)
    expected_field_keys = ['name', 'favorite_number', 'favorite_drink']
    assert validator.identity == identity
    assert set(validator.spec.keys()) == set(expected_field_keys)
