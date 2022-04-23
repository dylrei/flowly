from flowly.stores.names import NameStore


# Import child (not grandchild) namespaces


executors_namespace = NameStore.register(
    unique_name=__name__,
    file_path=__file__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
)


# Import modules containing actions for this namespace
if executors_namespace:
    from .test_identified import test_fx
