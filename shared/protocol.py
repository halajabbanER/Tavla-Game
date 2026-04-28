import json


def encode_message(data):
    return json.dumps(data).encode()


def decode_message(data):
    return json.loads(data.decode())