from flowly.constants.testing import TestingKeyword
from flowly.stores.names import NameStore
from flowly.testing.method import TestMethodBase


class TestMethodExecutor(TestMethodBase):
    def test_two_step(self):
        self.run_test_cases(
            namespace=NameStore.get_namespace('flowly.tests.content_root.sales'),
            method_identity='sales/cash::make_cash_sale==1.0',
            test_cases=[
                # First Step
                {
                    TestingKeyword.PROVIDED: {
                        'customer': 'finance/lists::CUST-123',
                        'items': ['sales/items::ITEM-777', 'sales/items::ITEM-888', 'sales/items::ITEM-999']
                    },
                    TestingKeyword.EXPECTED: {
                        'order_total': 3.14
                    }
                },
                # Second Step
                {
                    TestingKeyword.PROVIDED: {
                        'cash_tendered': 5.00
                    },
                    TestingKeyword.EXPECTED: {
                        'customer': 'finance/lists::CUST-123',
                        'order_number': 'ORD-1234',
                        'total_cost': 3.14
                    }
                },
            ]
        )
