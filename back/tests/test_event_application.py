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
application_id_tested = str()


class TestManageEventApplication(unittest.TestCase):
    def test_event_application_creation(self):
        body = {
            "record_number": "1",
            "client_name": "elina",
            "event_type": "party",
            "description": "none",
            "from_date": "2020/10/23",
            "to_date": "2020/10/30",
            "expected_number_attendees": "20",
            "planned_budget": "2000",
            "decorations": "balloon",
            "food_drinks": "BBQ, dessert and cider",
            "filming_photos": "yes",
            "music": "pop music",
            "posters_art_work": "none",
            "computer_related_issues": "none",
            "other_needs": "none"
        }

        username, password = "matthieu", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }

        http_request.request("POST", "/event_application_creation", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)
        global application_id_tested
        application_id_tested = json.loads(response.read().decode())["project_reference"]

    def test_event_application_retrieve(self):
        username, password = "jack", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        body = {"application_id": application_id_tested}
        http_request.request("GET", "/event_application_retrieve/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)


if __name__ == '__main__':
    unittest.main()
