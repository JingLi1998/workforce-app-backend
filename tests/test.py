import json
from unittest import TestCase, main
from pymongo import MongoClient
import requests
from test_seed import test_seed_db


def convert_json_id(collection):
    collection = json.dumps((collection), default=str).replace('"_id"', '"id"')
    return json.loads(collection)


class MainFunctionTests(TestCase):
    pass


class EmployeeApiTests(TestCase):
    def test_get_employees(self):
        test_seed_db()
        url = "http://localhost:3000/api/employees"
        response = requests.get(url, timeout=5)
        collection = convert_json_id(list(db["employees"].find()))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"employees": collection})

    def test_get_employee(self):
        test_seed_db()
        collection = convert_json_id(db["employees"].find_one({"salary_id": "m050317"}))
        url = f"http://localhost:3000/api/employees/{collection['id']}"
        response = requests.get(url, timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"employee": collection})

    def test_post_employee(self):
        test_seed_db(empty=True)
        url = "http://localhost:3000/api/employees"
        payload = json.dumps(
            {
                "salary_id": "m111111",
                "first_name": "James",
                "last_name": "Tinker",
                "role": "Poof Head",
                "projects": [],
            }
        )
        response = requests.post(url, data=payload, timeout=5)
        collection = convert_json_id(db["employees"].find_one({"salary_id": "m111111"}))
        del collection["id"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.text), {"employee added": collection})

    def test_put_employee(self):
        test_seed_db()
        collection = convert_json_id(db["employees"].find_one({"salary_id": "m050317"}))
        url = f"http://localhost:3000/api/employees/{collection['id']}"
        payload = json.dumps(
            {
                "salary_id": "m050317",
                "first_name": "James",
                "last_name": "Tinker",
                "role": "Poof Head",
                "projects": [],
            }
        )
        response = requests.put(url, data=payload, timeout=5)
        collection = convert_json_id(db["employees"].find_one({"salary_id": "m050317"}))
        del collection["id"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"employee": collection})

    def test_delete_employee(self):
        test_seed_db()
        collection = convert_json_id(db["employees"].find_one({"salary_id": "m050317"}))
        url = f"http://localhost:3000/api/employees/{collection['id']}"
        response = requests.delete(url, timeout=5)
        self.assertEqual(response.status_code, 204)

    def test_employee_add_project(self):
        test_seed_db()
        employee = convert_json_id(db["employees"].find_one({"salary_id": "m050317"}))
        project = convert_json_id(
            db["projects"].find_one({"name": "Windows 10 Migration"})
        )
        url = f"http://localhost:3000/api/employees/{employee['id']}/projects/{project['id']}"
        response = requests.patch(url, timeout=5)
        self.assertEqual(response.status_code, 200)

    def test_employee_add_department(self):
        test_seed_db()
        employee = convert_json_id(db["employees"].find_one({"salary_id": "m050317"}))
        department = convert_json_id(
            db["departments"].find_one({"name": "Financial Markets"})
        )
        url = f"http://localhost:3000/api/employees/{employee['id']}/departments/{department['id']}"
        response = requests.patch(url, timeout=5)
        self.assertEqual(response.status_code, 200)


class DepartmentApiTests(TestCase):
    def test_get_departments(self):
        test_seed_db()
        url = "http://localhost:3000/api/departments"
        response = requests.get(url, timeout=5)
        collection = convert_json_id(list(db["departments"].find()))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"departments": collection})

    def test_get_department(self):
        test_seed_db()
        collection = convert_json_id(
            db["departments"].find_one({"name": "Financial Markets"})
        )
        url = f"http://localhost:3000/api/departments/{collection['id']}"
        response = requests.get(url, timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"department": collection})

    def test_post_department(self):
        test_seed_db(empty=True)
        url = "http://localhost:3000/api/departments"
        payload = json.dumps(
            {"name": "Financial Markets", "location": "Kent St", "employees": []}
        )
        response = requests.post(url, data=payload, timeout=5)
        collection = convert_json_id(
            db["departments"].find_one({"name": "Financial Markets"})
        )
        del collection["id"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.text), {"department added": collection})

    def test_put_department(self):
        test_seed_db()
        collection = convert_json_id(
            db["departments"].find_one({"name": "Financial Markets"})
        )
        url = f"http://localhost:3000/api/departments/{collection['id']}"
        payload = json.dumps(
            {
                "name": "Pop Tarts",
                "location": "My Stomach",
                "employees": [],
                "projects": [],
            }
        )
        response = requests.put(url, data=payload, timeout=5)
        collection = convert_json_id(db["departments"].find_one({"name": "Pop Tarts"}))
        del collection["id"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"department": collection})

    def test_delete_department(self):
        test_seed_db()
        collection = convert_json_id(
            db["departments"].find_one({"name": "Financial Markets"})
        )
        url = f"http://localhost:3000/api/departments/{collection['id']}"
        response = requests.delete(url, timeout=5)
        self.assertEqual(response.status_code, 204)

    def test_department_add_employee(self):
        test_seed_db()
        department = convert_json_id(
            db["departments"].find_one({"name": "Financial Markets"})
        )
        employee = convert_json_id(db["employees"].find_one({"salary_id": "m050317"}))
        url = f"http://localhost:3000/api/departments/{department['id']}/employees/{employee['id']}"
        response = requests.patch(url, timeout=5)
        self.assertEqual(response.status_code, 200)

    def test_department_add_project(self):
        test_seed_db()
        department = convert_json_id(
            db["departments"].find_one({"name": "Financial Markets"})
        )
        project = convert_json_id(
            db["projects"].find_one({"name": "Windows 10 Migration"})
        )
        url = f"http://localhost:3000/api/departments/{department['id']}/projects/{project['id']}"
        response = requests.patch(url, timeout=5)
        self.assertEqual(response.status_code, 200)


class ProjectsApiTests(TestCase):
    def test_get_projects(self):
        test_seed_db()
        url = "http://localhost:3000/api/projects"
        response = requests.get(url, timeout=5)
        collection = convert_json_id(list(db["projects"].find()))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"projects": collection})

    def test_get_project(self):
        test_seed_db()
        collection = convert_json_id(
            db["projects"].find_one({"name": "Windows 10 Migration"})
        )
        url = f"http://localhost:3000/api/projects/{collection['id']}"
        response = requests.get(url, timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"project": collection})

    def test_post_project(self):
        test_seed_db(empty=True)
        url = "http://localhost:3000/api/projects"
        payload = json.dumps(
            {
                "name": "Windows 10 Migration",
                "description": "Test description!",
                "employees": [],
            }
        )
        response = requests.post(url, data=payload, timeout=5)
        collection = convert_json_id(
            db["projects"].find_one({"name": "Windows 10 Migration"})
        )
        del collection["id"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.text), {"project added": collection})

    def test_put_project(self):
        test_seed_db()
        collection = convert_json_id(
            db["projects"].find_one({"name": "Windows 10 Migration"})
        )
        url = f"http://localhost:3000/api/projects/{collection['id']}"
        payload = json.dumps(
            {"name": "Pop Tarts", "description": "Are very tasty!", "employees": []}
        )
        response = requests.put(url, data=payload, timeout=5)
        collection = convert_json_id(db["projects"].find_one({"name": "Pop Tarts"}))
        del collection["id"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), {"project": collection})

    def test_delete_project(self):
        test_seed_db()
        collection = convert_json_id(
            db["projects"].find_one({"name": "Windows 10 Migration"})
        )
        url = f"http://localhost:3000/api/projects/{collection['id']}"
        response = requests.delete(url, timeout=5)
        self.assertEqual(response.status_code, 204)

    def test_project_add_department(self):
        test_seed_db()
        project = convert_json_id(
            db["projects"].find_one({"name": "Windows 10 Migration"})
        )
        department = convert_json_id(
            db["departments"].find_one({"name": "Financial Markets"})
        )
        url = f"http://localhost:3000/api/projects/{project['id']}/departments/{department['id']}"
        response = requests.patch(url, timeout=5)
        self.assertEqual(response.status_code, 200)

    def test_project_add_employee(self):
        test_seed_db()
        project = convert_json_id(
            db["projects"].find_one({"name": "Windows 10 Migration"})
        )
        employee = convert_json_id(db["employees"].find_one({"salary_id": "m050317"}))
        url = f"http://localhost:3000/api/projects/{project['id']}/employees/{employee['id']}"
        response = requests.patch(url, timeout=5)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    db = MongoClient()["testdb"]
    main()
