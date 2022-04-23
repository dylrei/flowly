from flowly.stores.names import NameStore

# Import child (not grandchild) namespaces


ffio_core_namespace = NameStore.register(
    unique_name=__name__,
    file_path=__file__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
)

# Import modules containing actions for this namespace
from .math import add, subtract, multiply, divide