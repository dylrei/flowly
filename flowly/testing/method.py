from django.test import TestCase

from flowly.constants.payload import PayloadKey
from flowly.constants.testing import TestingKeyword
from flowly.stores.names import NameStore
from flowly.utils.json import unfloat
from flowly.utils.payload import is_uuid


class TestMethodBase(TestCase):
    def run_test_cases(self, namespace, method_identity, test_cases, break_before=False):
        method = namespace.get_method(method_identity)
        state = None
        if break_before:
            import ipdb; ipdb.set_trace()
        for tc in test_cases:
            result = method.run(
                data_provided=unfloat(tc[TestingKeyword.PROVIDED]),
                state_identity=state,
                namespace=namespace
            )
            self.assertEqual(result[PayloadKey.REQUEST][PayloadKey.METHOD], method_identity)
            self.assertEqual(result[PayloadKey.REQUEST][PayloadKey.NAMESPACE], namespace.unique_name)
            self.assertTrue(is_uuid(result[PayloadKey.REQUEST][PayloadKey.STATE]))
            self.assertEqual(result[PayloadKey.DATA], tc[TestingKeyword.EXPECTED])
            if result[PayloadKey.REQUEST][PayloadKey.COMPLETED]:
                self.assertEqual(result[PayloadKey.NEXT], {})
            else:
                state = result[PayloadKey.NEXT][PayloadKey.STATE]
                method_identity = result[PayloadKey.NEXT][PayloadKey.METHOD]
                namespace = NameStore.get_namespace(result[PayloadKey.NEXT][PayloadKey.NAMESPACE])
                method = namespace.get_method(method_identity)
