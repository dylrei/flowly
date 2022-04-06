import yaml

from . import get_test_loader


def _test_tag_configuration(tag_klass, document, expected_value):
    obj = yaml.load(document, Loader=get_test_loader(tag_klass))
    assert obj.__class__.__name__ == tag_klass.tag_name[1:]
    assert obj.value == expected_value

# todo: test new tag base classes, don't just remove old tests ;)