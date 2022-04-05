from ...executors.identified import identified_executor
from ...stores.identified_executor import IdentifiedExecutorStore


def test_store_happy_path():
    this_domain = __name__.replace('/', '.')
    first_version = '1.1'
    second_version = '1.2'

    @identified_executor(f'{this_domain}::test_fx@@{first_version}')
    def some_fx(x):
        return x + 5

    @identified_executor(f'{this_domain}::test_fx@@{second_version}')
    def some_other_version(x):
        return x + 25

    arg = 10
    assert IdentifiedExecutorStore.use(f'{this_domain}::test_fx@@{first_version}')(arg) == some_fx(arg)
    assert IdentifiedExecutorStore.use(f'{this_domain}::test_fx@@{second_version}')(arg) == some_other_version(arg)


def test_store_fail_path():
    try:
        @identified_executor('bogus/path::test_fx@@1.1')
        def some_fx(x):
            return x + 5
        success = True
    except RuntimeError as err:
        success = False
        assert 'Executor identity does not match location of executor declaration' in str(err)
    assert success is False