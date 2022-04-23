from ...stores.names import NameStore


# Import child (not grandchild) namespaces
from .core import core_namespace
from .examples import examples_namespace
from .executors import executors_namespace
from .sales import sales_namespace
from .specifications import specifications_namespace
from .test_cases import test_cases_namespace


ffio_namespace = NameStore.register(
    unique_name=__name__,
    file_path=__file__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
)


# Import modules containing actions for this namespace
