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
event_id_tested = list()
financial_manager_feedback = "Project seems unfeasible financially"


class TestManageEvent(unittest.TestCase):
    def test_event_creation(self):
        body = {
            "client_name": "elina",
            "event_type": "party",
            "from_date": "2020/10/23",
            "to_date": "2020/10/30",
            "expected_number_attendees": "20",
            "preferences": "parties"
        }

        username, password = "alicia", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }

        http_request.request("POST", "/event_creation/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)

    def test_retrieve(self):
        username, password = "matthieu", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }

        http_request.request("GET", "/review_event_creation/", headers=header)
        response = http_request.getresponse()
        decoded_response = json.loads(response.read().decode())
        print(decoded_response)
        event_ids = list()
        for event in decoded_response.values():
            event_ids = [e["record_number"] for e in event]
        global event_id_tested
        event_id_tested = event_ids[0]
        self.assertEqual(response.status, 200)

    def test_review(self):
        username, password = "matthieu", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response["token"])
        }
        body = {
            "record_number": "{}".format(event_id_tested),
            "status": "accepted"
        }

        http_request.request("PUT", "/review_event_creation/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)

    def test_review_feedback(self):
        username, password = "karl", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response["token"])
        }
        body = {
            "record_number": "{}".format(event_id_tested),
            "feedback": financial_manager_feedback
        }
        http_request.request("PUT", "/review_event_creation/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        print(response.read().decode())
        self.assertEqual(response.status, 200)

    def test_review_finalize(self):
        username, password = "mike", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response["token"])
        }
        body = {
            "record_number": "{}".format(event_id_tested),
            "status": "dismissed"
        }
        http_request.request("PUT", "/review_event_creation/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)
        http_request.request("DELETE", "/review_event_creation/", headers=header, body=json.dumps(body))
        deletion_response = http_request.getresponse()
        self.assertEqual(deletion_response.status, 200)


if __name__ == '__main__':
    unittest.main()
