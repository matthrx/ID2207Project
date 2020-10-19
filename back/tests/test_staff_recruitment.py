import json, http.client, unittest

from back.tests.utils import authenticate_client


address_server = "127.0.0.1"
port_server = 8080


http_request = http.client.HTTPConnection(
            host=address_server,
            port=port_server
        )

staff_request_id = str()


class TestStaffRecruitment(unittest.TestCase):
    def test_create_staff_request(self):
        username, password = "natalie", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        body = {
            "is_full_time": "true",
            "request_department": "production",
            "year_experience_min": 5,
            "job_title": "Photographer",
            "job_description": "Take photos at a party wedding"
        }
        http_request.request("POST", "/create_staff_request/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)

    def test_retrieve_staff_request(self):
        username, password = "simon", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        http_request.request('GET', "/review_staff_request/", headers=header, body=json.dumps(dict()))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)
        decoded_response = json.loads(response.read().decode()).values()
        staff_requests = list()
        for staff in decoded_response:
            staff_requests = [s["staff_request_id"] for s in staff]
        global staff_request_id
        staff_request_id = staff_requests[0]

    def test_update_staff_request(self):
        username, password = "simon", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        body = {
            "staff_request_id": staff_request_id,
            "status": "done"
        }
        http_request.request('PUT', "/review_staff_request/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)


if __name__ == '__main__':
    unittest.main()