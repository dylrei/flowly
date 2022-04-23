from flowly.constants.identity import IdentityDelimeter
from flowly.constants.testing import TestingKeyword
from flowly.models.unit_testing import Service, Customer
from flowly.testing.method import TestMethodBase
from flowly.tests.content_root import sales_namespace


class TestMethodExecutorWithMaterials(TestMethodBase):
    def test_new_service_order(self):
        cst1 = Customer.objects.create(name='Miles O’Brien', unique_id='CUST-333')
        srv1 = Service.objects.create(name='Modulate carrier wave', unique_id='SRVC-378')
        srv2 = Service.objects.create(name='Realign power couplings', unique_id='SRVC-1701')

        self.run_test_cases(
            namespace=sales_namespace,
            method_identity='sales/service::start_service_order==1.0',
            test_cases=[
                # First Step
                {
                    TestingKeyword.PROVIDED: {
                        'customer': f'{sales_namespace.unique_name}{IdentityDelimeter.NAMESPACE}{cst1.unique_id}',
                        'services': [f'{sales_namespace.unique_name}{IdentityDelimeter.NAMESPACE}{srv1.unique_id}',
                                     f'{sales_namespace.unique_name}{IdentityDelimeter.NAMESPACE}{srv2.unique_id}',
                                     f'{sales_namespace.unique_name}{IdentityDelimeter.NAMESPACE}{srv2.unique_id}']
                    },
                    TestingKeyword.EXPECTED: {
                        'service_order': {
                            'identity': f'{sales_namespace.unique_name}{IdentityDelimeter.NAMESPACE}SO-000001',
                            'number': 'SO-000001',
                            'status': 'pending'
                        }
                    }
                },
                # Second Step
                {
                    TestingKeyword.PROVIDED: {
                        'approved': True
                    },
                    TestingKeyword.EXPECTED: {
                        'service_order': {
                            'identity': f'{sales_namespace.unique_name}{IdentityDelimeter.NAMESPACE}SO-000001',
                            'number': 'SO-000001',
                            'status': 'approved'
                        }
                    }
                },
            ]
        )
