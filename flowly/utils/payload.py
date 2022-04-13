import hashlib
import json


def is_json(value):
    if not isinstance(value, str):
        return False
    try:
        json.loads(value)
        return True
    except json.JSONDecodeError:
        return False


def sort_json(json_data):
    return json.dumps(json.loads(json_data), sort_keys=True).encode('utf-8')


def sort_and_jsonify_data(data):
    if is_json(data):
        return sort_json(data)
    return json.dumps(data, sort_keys=True).encode('utf-8')


def hash_data(data):
    return hashlib.md5(sort_and_jsonify_data(data)).hexdigest()
