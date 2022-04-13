from flowly.executors.identified import identified_executor


@identified_executor('examples/hello_world::say_hello==production')
@identified_executor('examples/hello_world::say_hello==1.0')
def say_hello_1_0(name=None):
    if name is None:
        name = 'you beautiful person'
    return f'Hello, {name}!'
