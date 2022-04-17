from ffio import root_namespace, ffio_namespace
from flowly.stores.names import Namespace


def test_root_namespace():
    assert isinstance(root_namespace, Namespace)
    assert root_namespace.unique_name == ''
    assert root_namespace.canonical == 'ff.flowflow.io'
    assert root_namespace.source == 'github.com:dylrei/flowly.git'


def test_ffio_namespace():
    assert isinstance(ffio_namespace, Namespace)
    assert ffio_namespace.unique_name == 'ffio'
    assert ffio_namespace.canonical == 'ff.flowflow.io'
    assert ffio_namespace.source == 'github.com:dylrei/flowly.git'
