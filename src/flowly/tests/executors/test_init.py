from ...executors import versioned_executor


@versioned_executor
def example_function():
    def v1_0(*args, **kwargs):
        return f'v1.0: got {args} {kwargs}'

    def v1_1(*args, **kwargs):
        return f'v1.1: got {args} {kwargs}'

    def production(*args, **kwargs):
        return v1_0(*args, **kwargs)

    def default(*args, **kwargs):
        return v1_0(*args, **kwargs)

    def testing(*args, **kwargs):
        return v1_1(*args, **kwargs)

    return locals()


def test_versioned_executor():
    v1_0_expected = "v1.0: got ('a', 'b', 'c') {'foo': 'bar'}"
    v1_1_expected = "v1.1: got ('a', 'b', 'c') {'foo': 'bar'}"

    assert example_function('a', 'b', 'c', foo='bar') == v1_0_expected
    assert example_function('a', 'b', 'c', foo='bar', _version='v1_0') == v1_0_expected
    assert example_function('a', 'b', 'c', foo='bar', _version='default') == v1_0_expected
    assert example_function('a', 'b', 'c', foo='bar', _version='production') == v1_0_expected

    assert example_function('a', 'b', 'c', foo='bar', _version='v1_1') == v1_1_expected
    assert example_function('a', 'b', 'c', foo='bar', _version='testing') == v1_1_expected
