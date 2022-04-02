import yaml


def get_test_loader(tag_klass):
    loader = yaml.SafeLoader
    loader.add_constructor(tag_klass.tag_name, tag_klass.constructor)
    return loader
