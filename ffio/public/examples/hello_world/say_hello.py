from datetime import date

from flowly.executors.identified import identified_executor


@identified_executor('public/examples/hello_world::say_hello==production')
@identified_executor('public/examples/hello_world::say_hello==1.0')
def say_hello_1_0(name=None):
    if name is None:
        name = 'you beautiful person'
    day_of_week = date.today().strftime('%A')
    return f'Hello, {name}, and happy {day_of_week}!'

