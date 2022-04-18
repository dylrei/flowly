from ffio import ffio_core_namespace
from flowly.constants.testing import TestingKeyword
from flowly.testing.method import TestMethodBase


class TestMultiplyFunctional(TestMethodBase):
    def test_multiply(self):
        self.run_test_cases(
            namespace=ffio_core_namespace,
            method_identity='core/tests/math::demonstrate_float_conversion==1.0',
            test_cases=[
                {
                    TestingKeyword.PROVIDED: {'numbers_to_multiply': (1, 4.1)},
                    TestingKeyword.EXPECTED: {'product': 4.1}
                },
                {
                    TestingKeyword.PROVIDED: {'numbers_to_multiply': (10, 4.1)},
                    TestingKeyword.EXPECTED: {'product': 41.0}
                },
                # this next case shows that we are transparently converting all float inputs to decimal
                # before running methods/actions and back again for the response
                # normally:
                # >> 4.1 * 100
                # 409.99999999999994
                #
                # getting an answer of 410 is considered less surprising
                {
                    TestingKeyword.PROVIDED: {'numbers_to_multiply': (100, 4.1)},
                    # obviously...
                    TestingKeyword.EXPECTED: {'product': 410.0}
                },
            ]
        )
