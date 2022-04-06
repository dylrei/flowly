import yaml

from ...tags.base import LabelTag, ObjectTag


def get_test_loader(tag_klass):
    loader = yaml.SafeLoader
    loader.add_constructor(tag_klass.tag_name, tag_klass.constructor)
    return loader


def run_tag_tests(tag_klass, document, expected_tag_name, expected_klass_name, expected_value):
    obj = yaml.load(document, Loader=get_test_loader(tag_klass))
    assert obj.tag == expected_tag_name
    assert obj.__class__.__name__ == expected_klass_name
    if issubclass(tag_klass, LabelTag):
        assert obj.value == expected_value
    elif issubclass(tag_klass, ObjectTag):
        assert obj._value == expected_value
    else:
        raise RuntimeError(f'Missing a test for {tag_klass}')
