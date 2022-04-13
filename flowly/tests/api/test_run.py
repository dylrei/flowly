import json

from django.test import TestCase, Client

from ..content_root.examples.hello_world.say_hello import say_hello_1_0
from ...models.payload import Payload, Response


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
        assert Payload.objects.count() == 0
        assert Response.objects.count() == 0
        response = self.client.post('/api/run/',
                                    json.dumps(payload),
                                    content_type="application/json").json()
        assert response['method'] == method
        assert response['node'] is None
        assert 'state' in response
        assert response['data']['result']['response'] == 'Hello, Alia!'

        # posting the same data yields the same response, with no side effects
        assert Payload.objects.count() == 1
        assert Response.objects.count() == 1
        response2 = self.client.post('/api/run/',
                                     json.dumps(payload),
                                     content_type="application/json").json()
        assert response2['method'] == response['method']
        assert response2['node'] == response['node']
        assert 'state' in response2
        assert response2['data']['result']['response'] == response['data']['result']['response']
        # no new payloads or responses created
        assert Payload.objects.count() == 1
        assert Response.objects.count() == 1
