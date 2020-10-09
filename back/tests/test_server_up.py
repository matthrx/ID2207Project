import unittest
import http.client

address_server = "127.0.0.1"
port_server = 8080


http_request = http.client.HTTPConnection(
            host=address_server,
            port=port_server
        )


class ServerUp(unittest.TestCase):

    def test_server_up(self):
        http_request.request("GET", "/health/")
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)


if __name__ == '__main__':
    unittest.main()