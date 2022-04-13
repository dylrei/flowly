import datetime
import json

from django.test import TestCase, Client

from ..content_root.examples.hello_world.say_hello import say_hello_1_0
from ...constants.payload import PayloadKey
from ...models.payload import Payload, Response
from ...utils.payload import is_uuid


class RunApiTestCase(TestCase):
    def setUp(self):
        super(RunApiTestCase, self).setUp()
        self.client = Client()

    def test_run_api(self):
        method = 'examples::hello_world==1.0'
        payload = {
            'method': method,
            'data': {
                'name': 'Alia'
            }
        }
        api_args = '/api/run/', json.dumps(payload)
        api_kwargs = {'content_type': 'application/json'}

        assert Payload.objects.count() == 0
        assert Response.objects.count() == 0
        result = self.client.post(*api_args, **api_kwargs).json()
        assert result[PayloadKey.REQUEST][PayloadKey.METHOD] == method
        assert result[PayloadKey.REQUEST][PayloadKey.NODE] is None
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
