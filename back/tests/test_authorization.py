import unittest
import http.client
import json
from back.tests.utils import authenticate_client


address_server = "127.0.0.1"
port_server = 8080


http_request = http.client.HTTPConnection(
            host=address_server,
            port=port_server
        )

token = str()


class TestAuthorization(unittest.TestCase):

    def test_authorize_fm(self):
        username, password = "karl", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        http_request.request("GET", "/authorized_FM/", headers=header)
        response = http_request.getresponse()
        decoded_response = json.loads(response.read().decode())
        print(decoded_response)
        print(token)
        self.assertEqual(response.status, 200)


if __name__ == '__main__':
    unittest.main()
