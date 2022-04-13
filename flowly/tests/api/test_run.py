import json

from django.test import TestCase, Client

from ..content_root.examples.hello_world.say_hello import say_hello_1_0


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
        response = self.client.post('/api/run/',
                                    json.dumps(payload),
                                    content_type="application/json").json()
        assert response['method'] == method
        assert response['node'] is None
        assert 'state' in response
        assert response['data']['result']['response'] == 'Hello, Alia!'
