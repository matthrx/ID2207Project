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
        username, passowrd = "matthieu", "password"
        body = {
            "username": username,
            "password": passowrd
        }
        body_json = json.dumps(body)
        http_request.request('GET', '/authenticate/', body=body_json)
        response = http_request.getresponse()
        decoded_response = json.loads(response.read().decode())
        self.assertEqual(response.status, 200)
        self.assertEqual(decoded_response["username"], username)
        self.assertIsNot(decoded_response["token"], str())
        global token
        token = decoded_response["token"]
        return token

    def test_client_is_connected(self):
        header = {
            'Authorization': 'Bearer {}'.format(token)
        }
        http_request.request("GET", "/connected/", headers=header)
        response = http_request.getresponse()
        print(response.read())
        self.assertEqual(response.status, 200)


if __name__ == '__main__':
    unittest.main()
