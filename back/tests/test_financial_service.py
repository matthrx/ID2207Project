import unittest
import http.client
from back.tests.utils import authenticate_client
import json

address_server = "127.0.0.1"
port_server = 8080


http_request = http.client.HTTPConnection(
            host=address_server,
            port=port_server
        )

project_reference = str()
financial_request_id = str()


class TestFinancialRequest(unittest.TestCase):

    def test_application_retrieve(self):
        username, password = "jack", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        http_request.request("GET", "/event_application_retrieve/", headers=header, body=json.dumps({}))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)
        decoded_response = json.loads(response.read().decode())
        applications_references = list()
        if not decoded_response["applications"]:
            raise AssertionError("No application exists, we can't launch financial request creation, further tests will fail")
        for each_application in decoded_response["applications"]:
            applications_references = [e["project_reference"] for e in each_application]
        global project_reference
        project_reference = applications_references[0]

    def test_create_financial_request(self):
        username, password = "jack", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        body = {
            "request_department": "production",
            "project_reference": project_reference,
            "required_amount": 5000,
            "reason": "Need more resources"
        }
        http_request.request("POST", "/create_financial_request/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)
        global financial_request_id
        financial_request_id = json.loads(response.read().decode())["financial_request_id"]
        self.assertIsNot(financial_request_id, str())

    def test_retrieve_financial_request(self):
        username, password = "karl", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        http_request.request("GET", "/review_financial_request/", headers=header, body=json.dumps(dict()))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)
        financial_ids = list()
        financial_requests = json.loads(response.read().decode())
        for financial_request in financial_requests["financial_requests"]:
            financial_ids.append(financial_request.get("financial_request_id", str()))
        if financial_request_id != str():
            self.assertIn(financial_request_id, financial_ids)
        else:
            self.assertGreaterEqual(len(financial_ids), 0)

    def test_update_financial_request(self):
        username, password = "karl", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        body = {
            "financial_request_id": financial_request_id,
            "status": "done"
        }
        http_request.request("PUT", "/review_financial_request/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        print(response.read().decode())
        self.assertEqual(response.status, 200)


if __name__ == '__main__':
    unittest.main()