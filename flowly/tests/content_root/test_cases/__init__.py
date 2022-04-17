from flowly.stores.names import NameStore

test_cases_namespace = NameStore.register(
    unique_name=__name__,
    file_path=__file__,
    canonical='ff.flowflow.io',
    source='github.com:dylrei/flowly.git',
)