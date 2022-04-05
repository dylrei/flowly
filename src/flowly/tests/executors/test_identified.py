from ...executors.identified import identified_executor
from ...stores.identified_executor import IdentifiedExecutorStore


@identified_executor('executors/test_identified::test_fx@@1.1')
def one_implementation(x):
    return x + 5

@identified_executor('executors/test_identified::test_fx@@production')
@identified_executor('executors/test_identified::test_fx@@1.2')
def another_implementation(x):
    return x * 3

@identified_executor('executors/test_identified::test_fx@@testing')
@identified_executor('executors/test_identified::test_fx@@1.3')
def yet_another_implementation(x):
    return x * 3 + 5

@identified_executor('executors/test_identified::test_fx@@ruo')
def do_not_use_this_version_unless_you_are_me(x):
    return f'What shall I do with a/an {x}?'


def test_identified_executor():
    arg = 5

    assert one_implementation(arg) == 10
    assert another_implementation(arg) == 15
    assert yet_another_implementation(arg) == 20
    assert do_not_use_this_version_unless_you_are_me(arg) == 'What shall I do with a/an 5?'

    store = IdentifiedExecutorStore
    assert store.use('executors/test_identified::test_fx@@1.1')(arg) == one_implementation(arg)
    assert store.use('executors/test_identified::test_fx@@production')(arg) == another_implementation(arg)
    assert store.use('executors/test_identified::test_fx@@1.2')(arg) == another_implementation(arg)
    assert store.use('executors/test_identified::test_fx@@testing')(arg) == yet_another_implementation(arg)
    assert store.use('executors/test_identified::test_fx@@1.3')(arg) == yet_another_implementation(arg)
    assert store.use('executors/test_identified::test_fx@@ruo')(arg) == do_not_use_this_version_unless_you_are_me(arg)
