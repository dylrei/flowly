from django.test import TestCase

from flowly.constants.testing import TestingKeyword
from flowly.utils.json import unfloat


class TestActionBase(TestCase):
    def run_test_cases(self, namespace, action_identity, test_cases):
        action = namespace.get_executor(action_identity)
        for tc in test_cases:
            args = unfloat(tc.get(TestingKeyword.ARGS, tuple()))
            kwargs = unfloat(tc.get(TestingKeyword.KWARGS, dict()))
            result = action(*args, **kwargs)
            self.assertEqual(result, unfloat(tc[TestingKeyword.EXPECTED]))
