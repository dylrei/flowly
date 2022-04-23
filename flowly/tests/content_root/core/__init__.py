from flowly.stores.names import NameStore


# Import child (not grandchild) namespaces


core_namespace = NameStore.register(
    unique_name=__name__,
    file_path=__file__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
)


# Import modules containing actions for this namespace
if core_namespace:
    from .math import subtract
