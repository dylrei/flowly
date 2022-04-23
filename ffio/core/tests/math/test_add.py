from ffio.core import ffio_core_namespace
from flowly.constants.testing import TestingKeyword
from flowly.testing.action import TestActionBase


class TestAddAction(TestActionBase):
    def test_add_1_0(self):
        self.run_test_cases(
            namespace=ffio_core_namespace,
            action_identity='core/math::add==1.0',
            test_cases=[
                {
                    TestingKeyword.ARGS: [(1, 3, 5, 6.1)],
                    TestingKeyword.EXPECTED: 15.1
                },
                {
                    TestingKeyword.KWARGS: {'numbers': (1, 3, 5, 6.1)},
                    TestingKeyword.EXPECTED: 15.1
                },
            ]
        )