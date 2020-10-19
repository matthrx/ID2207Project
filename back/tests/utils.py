import http
import json


def authenticate_client(username: str, password: str, http_request: http.client.HTTPConnection):
    body = {
        "username": username,
        "password": password
    }
    body_json = json.dumps(body)
    http_request.request('GET', '/authenticate/', body=body_json)
    response = http_request.getresponse()
    decoded_response = json.loads(response.read().decode())
    if response.status == 200:
        return decoded_response
    else:
        raise AssertionError("Authentication not done: {}".format(decoded_response.get("error")))