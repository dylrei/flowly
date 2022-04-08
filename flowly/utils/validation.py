def validate_expected_and_required_values(provided_values, expected_values=None, required_values=None,
                                          descriptor='value'):
    if expected_values is None:
        expected_values = list()

    if required_values is None:
        required_values = list()

    for arg in [expected_values, required_values, provided_values]:
        if isinstance(arg, str):
            raise TypeError(f'Expecting non-string collection, got {arg}')

    required = set(required_values)
    # if a name is required, it is presumed to also be expected
    expected = set(expected_values).union(required)
    provided = set(provided_values)

    missing = required - provided
    unexpected = provided - expected

    if missing:
        raise RuntimeError(f'Required {descriptor}(s) missing: {missing}; Provided: {provided}')

    if unexpected:
        raise RuntimeError(f'Unexpected {descriptor}(s) provided: {unexpected}; Expected: {expected}')

    return True


def int_or_none(value):
    if value is not None:
        return int(value)