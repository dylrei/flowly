from ..constants.document import YamlKeyword, DataType
from ..constants.tags import TagName
from ..utils.validation import validate_expected_and_required_values, int_or_none


class InputValidator(object):
    def __init__(self, identity, loaded_yaml):
        self.identity = identity
        self.spec = loaded_yaml[TagName.INPUT]

    # todo: need to load !Validators and do something useful with them

    def validate(self, data_node, namespace):
        if isinstance(data_node, dict):
            return _validate_dict(self.spec, data_node, namespace)
        else:
            return _validate_list(self.spec, data_node, namespace)

def _validate_dict(spec_part, data_part, namespace):
    if 'id' in spec_part:
        spec_part = namespace.get_validator(spec_part['id'])

    validate_expected_and_required_values(
        expected_values=spec_part.keys(),
        required_values=[k for k, v in spec_part.items() if v.get(YamlKeyword.REQUIRED)],
        provided_values=data_part.keys(),
        descriptor='data/payload key'
    )
    # having confirmed that all required fields are provided and all provided fields are allowed,
    # we only need to step through the data that is actually provided
    for field_name, data_value in data_part.items():
        spec_details = spec_part[field_name]
        if spec_details[YamlKeyword.DATA_TYPE] == DataType.OBJECT:
            _validate_dict(spec_details, data_value)
        elif spec_details[YamlKeyword.DATA_TYPE] == DataType.ARRAY:
            _validate_list(spec_details, data_value, namespace)
        else:
            _validate_scalar(spec_details, data_value)
    return True

def _validate_scalar(spec_part, data_part):
    expected_data_type = spec_part[YamlKeyword.DATA_TYPE]
    validation_failure = False
    if expected_data_type == DataType.STRING:
        if not isinstance(data_part, str):
            validation_failure = True
    elif expected_data_type == DataType.INTEGER:
        if not isinstance(data_part, int):
            validation_failure = True
    elif expected_data_type == DataType.FLOAT:
        if not isinstance(data_part, float):
            validation_failure = True
    elif expected_data_type == DataType.BOOLEAN:
        if not isinstance(data_part, bool):
            validation_failure = True
    elif expected_data_type == DataType.OTHER:
        raise NotImplementedError(f'Need to implement validation handling for DataType.OTHER')
    else:
        raise NotImplementedError(f'No validation handling implemented for data_type {expected_data_type}')
    if validation_failure:
        raise RuntimeError(f'Expected {expected_data_type}, got: {data_part} (type: {type(data_part)})')


def _validate_list(spec_part, data_part, namespace):
    min_size = int_or_none(spec_part.get(YamlKeyword.MIN_SIZE))
    max_size = int_or_none(spec_part.get(YamlKeyword.MAX_SIZE))
    count_elems_provided = len(data_part)
    if min_size and count_elems_provided < min_size:
        raise RuntimeError(f'Not enough elements provided; Required: {min_size}; Provided: {count_elems_provided}')
    if max_size and count_elems_provided > max_size:
        raise RuntimeError(f'Too many elements provided; Permitted: {max_size}; Provided: {count_elems_provided}')

    member_data_type = spec_part.get(YamlKeyword.MEMBER_DATA_TYPE)
    member_spec = spec_part.get(YamlKeyword.MEMBER_SPEC)
    if member_spec is not None and 'id' in member_spec:
        validator = namespace.get_validator(member_spec['id'])
        _ = [validator.validate(member, namespace) for member in data_part]
    else:
        if member_data_type == DataType.OBJECT:
            _ = [_validate_dict(member_spec, member, namespace) for member in data_part]
        elif member_data_type == DataType.ARRAY:
            _ = [_validate_list(member_spec, member, namespace) for member in data_part]
        else:
            _ = [_validate_scalar({YamlKeyword.DATA_TYPE: member_data_type}, member) for member in data_part]
