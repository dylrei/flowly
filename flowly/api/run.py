import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views import View

# from content_root import content_root
from ..models.payload import Payload, Response
from ..stores.method import MethodStore
from ..utils.payload import hash_data


class RunMethod(View):
    def post(self, request):
        # validate payload
        payload_data = json.loads(request.body)
        payload_hash = hash_data(payload_data)
        try:
            # if we've seen this payload already, idempotently repeat our last response
            payload = Payload.objects.get(md5=payload_hash)
            return JsonResponse(payload.response.data)
        except Payload.DoesNotExist:
            payload = Payload.objects.create(md5=payload_hash)
            method_executor = MethodStore.load(payload_data['method'])
            response_data = method_executor.run(payload_data.get('data'), payload_data.get('state'))
            Response.objects.create(payload=payload, data=response_data)
            return JsonResponse(response_data, encoder=DjangoJSONEncoder)
