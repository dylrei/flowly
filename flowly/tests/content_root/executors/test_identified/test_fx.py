from .....executors.identified import identified_executor


@identified_executor('executors/test_identified::test_fx==1.1')
def one_implementation(x):
    return x + 5


@identified_executor('executors/test_identified::test_fx==production')
@identified_executor('executors/test_identified::test_fx==1.2')
def another_implementation(x):
    return x * 3


@identified_executor('executors/test_identified::test_fx==testing')
@identified_executor('executors/test_identified::test_fx==1.3')
def yet_another_implementation(x):
    return x * 3 + 5


@identified_executor('executors/test_identified::test_fx==ruo')
def do_not_use_this_version_unless_you_are_me(x):
    return f'What shall I do with a/an {x}?'