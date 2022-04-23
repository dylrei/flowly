from ffio.core import ffio_core_namespace
from flowly.constants.testing import TestingKeyword
from flowly.testing.action import TestActionBase


class TestMultiplyAction(TestActionBase):
    def test_multiply_1_0(self):
        self.run_test_cases(
            namespace=ffio_core_namespace,
            action_identity='core/math::multiply==1.0',
            test_cases=[
                {
                    TestingKeyword.ARGS: ([1, 4.1],),
                    TestingKeyword.EXPECTED: 4.1
                },
                {
                    TestingKeyword.ARGS: ([10, 4.1],),
                    TestingKeyword.EXPECTED: 41.0
                },
                # note that floats are cast to decimal internally before calculations performed
                # normally, in Python:
                # >> 4.1 * 100
                # 409.99999999999994
                {
                    TestingKeyword.ARGS: ([100, 4.1],),
                    TestingKeyword.EXPECTED: 410
                },
            ]
        )