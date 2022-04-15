from flowly.stores.names import NameStore

sales_namespace = NameStore.register(
    unique_name='sales',
    file_path=__file__,
    module_path=__name__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
    actions=list(),
    namespaces=list()
)