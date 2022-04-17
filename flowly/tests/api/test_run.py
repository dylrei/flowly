import json

from django.test import TestCase, Client

from ...constants.payload import PayloadKey
from ...models.payload import Payload, Response
from ...utils.payload import is_uuid


class RunApiTestCase(TestCase):
    def setUp(self):
        super(RunApiTestCase, self).setUp()
        self.client = Client()

    def test_run_api(self):
        namespace = 'flowly.tests.content_root.examples'
        method = 'examples::hello_world==1.0'
        payload = {
            PayloadKey.METHOD: method,
            PayloadKey.NAMESPACE: 'flowly.tests.content_root.examples',
            PayloadKey.DATA: {
                'name': 'Alia'
            }
        }
        api_args = '/api/run/', json.dumps(payload)
        api_kwargs = {'content_type': 'application/json'}

        assert Payload.objects.count() == 0
        assert Response.objects.count() == 0
        result = self.client.post(*api_args, **api_kwargs).json()
        assert result[PayloadKey.REQUEST][PayloadKey.METHOD] == method
        assert result[PayloadKey.REQUEST][PayloadKey.NAMESPACE] == namespace
        assert is_uuid(result[PayloadKey.REQUEST][PayloadKey.STATE])
        assert result[PayloadKey.REQUEST][PayloadKey.COMPLETED] is True
        assert result[PayloadKey.DATA] == {'response': 'Hello, Alia!'}
        assert result[PayloadKey.NEXT] == {}
        assert PayloadKey.TIMESTAMP in result
        # this is the first time we've seen this payload
        assert result[PayloadKey.DUPLICATE] is False
        assert Payload.objects.count() == 1
        assert Response.objects.count() == 1

        # posting the same data yields the same response, with no side effects
        response2 = self.client.post(*api_args, **api_kwargs).json()
        assert response2[PayloadKey.REQUEST] == result[PayloadKey.REQUEST]
        assert response2[PayloadKey.DATA] == result[PayloadKey.DATA]
        assert response2[PayloadKey.NEXT] == result[PayloadKey.NEXT]
        # one small difference in the response, this is not our first time here
        assert response2[PayloadKey.DUPLICATE] is True
        # no new payloads or responses created
        assert Payload.objects.count() == 1
        assert Response.objects.count() == 1

    def test_multi_step_api_run(self):
        namespace = 'flowly.tests.content_root.sales'
        method = 'sales/cash::make_cash_sale==1.0'
        payload = {
            PayloadKey.METHOD: method,
            PayloadKey.NAMESPACE: namespace,
            PayloadKey.DATA: {
                'customer': 'finance/lists::CUST-123',
                'items': ['sales/items::ITEM-777', 'sales/items::ITEM-888', 'sales/items::ITEM-999']
            }
        }
        api_args = '/api/run/', json.dumps(payload)
        api_kwargs = {'content_type': 'application/json'}

        # first step
        result = self.client.post(*api_args, **api_kwargs).json()
        assert result[PayloadKey.REQUEST][PayloadKey.METHOD] == method
        assert result[PayloadKey.REQUEST][PayloadKey.NAMESPACE] == namespace
        assert is_uuid(result[PayloadKey.REQUEST][PayloadKey.STATE])
        assert result[PayloadKey.REQUEST][PayloadKey.COMPLETED] is False
        assert result[PayloadKey.DATA] == {'order_total': 3.14}
        assert result[PayloadKey.NEXT] == {k: v for k, v in result[PayloadKey.REQUEST].items() if
                                           k != PayloadKey.COMPLETED}
        assert PayloadKey.TIMESTAMP in result
        first_run_state_id = result[PayloadKey.REQUEST][PayloadKey.STATE]

        # second step
        payload = {
            PayloadKey.METHOD: method,
            PayloadKey.NAMESPACE: namespace,
            PayloadKey.DATA: {'cash_tendered': 5.00},
            PayloadKey.STATE: first_run_state_id,
            PayloadKey.NAMESPACE: namespace,
        }
        api_args = '/api/run/', json.dumps(payload)
        result2 = self.client.post(*api_args, **api_kwargs).json()
        assert result2[PayloadKey.REQUEST][PayloadKey.METHOD] == method
        assert result2[PayloadKey.REQUEST][PayloadKey.NAMESPACE] == namespace
        assert is_uuid(result2[PayloadKey.REQUEST][PayloadKey.STATE])
        assert result2[PayloadKey.REQUEST][PayloadKey.COMPLETED] is True
        assert result2[PayloadKey.DATA] == {'customer': 'finance/lists::CUST-123',
                                            'order_number': 'ORD-1234',
                                            'total_cost': 3.14}
        assert result2[PayloadKey.NEXT] == {}
        assert PayloadKey.TIMESTAMP in result2
