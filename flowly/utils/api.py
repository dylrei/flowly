import decimal
import json

from flowly.constants.payload import PayloadKey
from flowly.models import Payload, Response
from flowly.stores.names import NameStore
from flowly.utils.payload import hash_request_body


def api_run_method(request_body):
    # todo: auth stuff
    # todo: is canonical
    # todo: validate payload
    payload_hash = hash_request_body(request_body)
    try:
        # if we've seen this payload already, idempotently repeat our last response
        payload = Payload.objects.get(md5=payload_hash)
        return dict(payload.response.data, **{PayloadKey.DUPLICATE: True})
    except Payload.DoesNotExist:
        payload_data = json.loads(request_body, parse_float=decimal.Decimal)
        namespace = NameStore.get_namespace(payload_data[PayloadKey.NAMESPACE])
        method_executor = namespace.get_method(payload_data[PayloadKey.METHOD])
        response_data = method_executor.run(
            data_provided=payload_data.get(PayloadKey.DATA),
            state_identity=payload_data.get(PayloadKey.STATE),
            namespace=namespace
        )
        payload = Payload.objects.create(md5=payload_hash)
        Response.objects.create(payload=payload, data=response_data)
        return dict(payload.response.data, **{PayloadKey.DUPLICATE: False})