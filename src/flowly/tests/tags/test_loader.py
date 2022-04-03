from ...constants.tags import MethodSectionName
from ...tags.loader import load_yaml


sample_yaml = '''
- !META
  document_type: specification
  domain: sample_org/sample_namespace
  method_name: reference_specification
  version: 0.1
  status: testing

- !ALIASES
  # a place to store reusable YAML anchors
  - required_string: &required-string
    data_type: string
    required: true

- !INPUT
  input_keyword_one:
    <<: *required-string
    validators:
      - !Validator validator_identifier

- !BODY
  - !Step
    id: step_identifier
    step_kw_one: step_value_one
    body:
      - !Action
        id: action_identifier
        some_material: !Material material_id
        some_asset: !Asset asset_id
        some_data: !Data data_id
        some_literal: literal value
  - !Method
    id: method_identifier
    method_kw_one: method_value_one
    
- !RETURN
  return_keyword_one: return_value_one
'''

def test_load_yaml():
    result = load_yaml(sample_yaml)

    # note: we don't expect to get the "ALIASES" section, that's stripped out
    expected_keys = [MethodSectionName.META, MethodSectionName.INPUT, MethodSectionName.BODY, MethodSectionName.RETURN]

    # sanity comparison - is this right type and shape of stuff we're expecting?
    assert isinstance(result, dict) is True
    assert len(result) == len(expected_keys)
    for key in expected_keys:
        assert key in result
