from datetime import date

from flowly.constants.testing import TestingKeyword
from flowly.stores.names import NameStore
from flowly.testing.method import TestMethodBase


class TestHelloWorld(TestMethodBase):
    def test_1_0(self):
        day_of_week = date.today().strftime('%A')
        self.run_test_cases(
            namespace=NameStore.get_namespace('ffio.public'),
            method_identity='public/examples::hello_world==1.0',
            test_cases=[
                {
                    TestingKeyword.PROVIDED: {
                        'name': None
                    },
                    TestingKeyword.EXPECTED: {
                        'response': f'Hello, you beautiful person, and happy {day_of_week}!'
                    }
                },
                {
                    TestingKeyword.PROVIDED: {
                        'name': 'Alia'
                    },
                    TestingKeyword.EXPECTED: {
                        'response': f'Hello, Alia, and happy {day_of_week}!'
                    }
                }

            ]
        )