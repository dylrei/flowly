from flowly.documents.loader import load_yaml_document, _load_yaml


def load_yaml(document):
    return _load_yaml(document)


def run_tag_tests(document, expected_tag_name, expected_value):
    obj = load_yaml(document)
    assert obj.tag == expected_tag_name
    if hasattr(obj, 'tag_name'):
        assert obj.tag_name == expected_tag_name
    assert obj.value == expected_value
