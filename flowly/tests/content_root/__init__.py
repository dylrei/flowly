from .core import core_namespace
from .core.math import subtract
from .examples import examples_namespace
from .executors import executors_namespace
from .executors.test_identified import test_fx
from .sales import sales_namespace
from .specifications import specifications_namespace
from .test_cases import test_cases_namespace

from ...stores.names import NameStore

authorized_actions = [subtract, test_fx]

authorized_namespaces = [specifications_namespace, test_cases_namespace, sales_namespace, executors_namespace,
                         core_namespace, examples_namespace]

ffio_namespace = NameStore.register(
    unique_name='tests',
    file_path=__file__,
    module_path=__name__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
    actions=authorized_actions,
    namespaces=authorized_namespaces
)