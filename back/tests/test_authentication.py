import unittest
import http.client
import json

address_server = "127.0.0.1"
port_server = 8080


http_request = http.client.HTTPConnection(
            host=address_server,
            port=port_server
        )

token = str()


class TestAuthentication(unittest.TestCase):

    def test_client_exists(self):
        username, password = "matthieu", "password"
        response = authenticate_client(username, password, http_request)
        self.assertEqual(response["username"], username)
        self.assertIsNot(response["token"], str())
        global token
        token = response["token"]
        return token

    def test_client_is_connected(self):
        header = {
            'Authorization': 'Bearer {}'.format(token)
        }
        http_request.request("GET", "/connected/", headers=header)
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)


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

if __name__ == '__main__':
    unittest.main()
