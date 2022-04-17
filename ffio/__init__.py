#    "Namespaces are one honking great idea -- let's do more of those!"
#    -- The Zen of Python

from flowly.stores.names import NameStore

# Import child (not grandchild) namespaces
from ffio.public import public_namespace

ffio_namespace = NameStore.register(
    unique_name=__name__,
    file_path=__file__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
)

root_namespace = NameStore.register(
    unique_name='',
    file_path=__file__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
)

# Import modules containing actions for this namespace
from ffio.public.examples import hello_world
