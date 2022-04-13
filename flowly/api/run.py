import json

from django.http import JsonResponse
from django.views import View

# from content_root import content_root
from ..stores.method import MethodStore


class RunMethod(View):
    def post(self, request):
        payload = json.loads(request.body)
        # validate payload
        # record payload, check for existing, provide idempotent response
        method_executor = MethodStore.load(payload['method'])
        return JsonResponse(method_executor.run(payload.get('data'), payload.get('state')))