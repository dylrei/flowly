from flowly.stores.names import NameStore


# Import child (not grandchild) namespaces


examples_namespace = NameStore.register(
    unique_name=__name__,
    file_path=__file__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
)


# Import modules containing actions for this namespace
if examples_namespace:
    from .hello_world import say_hello  # ...to my little friend
