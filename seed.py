import pymongo
import os

seed_employees = [
    {
        "salary_id": "m050317",
        "first_name": "Jing",
        "last_name": "Li",
        "role": "Application Developer",
        "projects": [],
    },
    {
        "salary_id": "m112233",
        "first_name": "Luna",
        "last_name": "Gao",
        "role": "Business Analyst",
        "projects": [],
    },
    {
        "salary_id": "m998877",
        "first_name": "Laura",
        "last_name": "Jin",
        "role": "Network Engineer",
        "projects": [],
    },
]

seed_departments = [
    {
        "name": "Specialist Finance Technology",
        "location": "Barangaroo",
        "employees": [],
        "projects": [],
    },
    {
        "name": "Financial Markets",
        "location": "Kent St",
        "employees": [],
        "projects": [],
    },
    {
        "name": "Data Centre Management",
        "location": "Kogarah",
        "employees": [],
        "projects": [],
    },
]

seed_projects = [
    {
        "name": "Windows 10 Migration",
        "description": "Convert all current systems and platforms to Windows 10",
        "employees": [],
    },
    {
        "name": "AppDynamics Rollout",
        "description": "Integrate AppDynamics to existing monitoring soltuions",
        "employees": [],
    },
    {
        "name": "Splunk Monitoring",
        "description": "Create automated alerts from Splunk queries",
        "employees": [],
    },
]


def seed_db(empty=False):
    db = pymongo.MongoClient(os.environ["DATABASE_URL"])["workforce_app"]
    db["employees"].drop()
    db["departments"].drop()
    db["projects"].drop()
    if not empty:
        db["employees"].insert_many(seed_employees)
        db["departments"].insert_many(seed_departments)
        db["projects"].insert_many(seed_projects)


if __name__ == "__main__":
    seed_db()
