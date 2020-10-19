import unittest
import json
import http.client

from back.tests.utils import authenticate_client

address_server = "127.0.0.1"
port_server = 8080


http_request = http.client.HTTPConnection(
            host=address_server,
            port=port_server
        )

project_reference = str()
tasks = list()


class TestTasks(unittest.TestCase):
    def test_application_retrieve(self):
        # 695e5341-793b-4f3e-aee6-d44fa254d9c8
        username, password = "jack", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        body = {}
        http_request.request("GET", "/event_application_retrieve/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        projects_references = list()
        for each_application in json.loads(response.read().decode()).values():
            projects_references = [e["project_reference"] for e in each_application]
        global project_reference
        project_reference = projects_references[0]
        self.assertEqual(response.status, 200)

    def test_task_creation(self):
        """
        Expecting project_reference, username the one assigned, priority and description
        :return:
        """
        username, password = "jack", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        body = {
            "project_reference": project_reference,
            "user_assigned": "chris",
            "description": "Create schedule for next meeting",
            "priority": "high"
        }
        http_request.request("POST", "/create_task/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)

    def test_task_retrieve(self):
        username, password = "chris", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        http_request.request("GET", "/retrieve_task/", headers=header, body=json.dumps(dict()))
        response = http_request.getresponse()
        decoded_response = json.loads(response.read().decode())
        for task in decoded_response["tasks"]:
            global tasks
            tasks.append(task["task_id"])
        self.assertGreaterEqual(len(tasks), 1)
        self.assertEqual(response.status, 200)

    def test_task_update(self):
        username, password = "chris", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        body = {
            "task_id": tasks[0],
            "status": "dismissed"
        }
        http_request.request("PUT", "/retrieve_task/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)

    def test_task_vdelete(self):
        username, password = "chris", "password"
        response = authenticate_client(username, password, http_request)
        header = {
            'Authorization': 'Bearer {}'.format(response.get("token"))
        }
        body = {
            "task_id": tasks[0],
        }
        http_request.request("DELETE", "/retrieve_task/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        self.assertEqual(response.status, 200)

if __name__ == '__main__':
    unittest.main()