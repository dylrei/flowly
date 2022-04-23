from datetime import date

from ffio.public.examples.hello_world.say_hello import say_hello_1_0


def test_say_hello_action():
    fx = say_hello_1_0
    test_name = 'Alia'
    day_of_week = date.today().strftime('%A')
    expected_response = f'Hello, Alia, and happy {day_of_week}!'
    assert fx(test_name) == expected_response

    test_name = None
    expected_response = f'Hello, you beautiful person, and happy {day_of_week}!'
    assert fx(test_name) == expected_response
