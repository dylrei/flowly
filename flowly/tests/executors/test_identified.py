from flowly.tests.content_root.executors.test_identified import test_fx
from flowly.tests.content_root.executors import executors_namespace as namespace

def test_identified_executor():
    arg = 5

    assert test_fx.one_implementation(arg) == 10
    assert test_fx.another_implementation(arg) == 15
    assert test_fx.yet_another_implementation(arg) == 20
    assert test_fx.do_not_use_this_version_unless_you_are_me(arg) == 'What shall I do with a/an 5?'

    assert namespace.get_executor('executors/test_identified::test_fx==1.1')(arg) == test_fx.one_implementation(arg)
    assert namespace.get_executor('executors/test_identified::test_fx==production')(arg) == test_fx.another_implementation(arg)
    assert namespace.get_executor('executors/test_identified::test_fx==1.2')(arg) == test_fx.another_implementation(arg)
    assert namespace.get_executor('executors/test_identified::test_fx==testing')(arg) == test_fx.yet_another_implementation(arg)
    assert namespace.get_executor('executors/test_identified::test_fx==1.3')(arg) == test_fx.yet_another_implementation(arg)
    assert namespace.get_executor('executors/test_identified::test_fx==ruo')(arg) == test_fx.do_not_use_this_version_unless_you_are_me(arg)
