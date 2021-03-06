import unittest
import http.client
from back.tests.utils import authenticate_client

address_server = "127.0.0.1"
port_server = 8080


http_request = http.client.HTTPConnection(
            host=address_server,
            port=port_server

        )
token = str()

class TestAuthentication(unittest.TestCase):

    def test_client_exists(self):
        username, password = "chris", "password"
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


if __name__ == '__main__':
    unittest.main()
