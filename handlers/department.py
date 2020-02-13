import json
from marshmallow.exceptions import ValidationError
from handlers.base import BaseHandler


class DepartmentsHandler(BaseHandler):
    """Departments Endpoint."""

    async def get(self):
        departments = await self.do_find(name="department")
        self.write({"departments": departments})

    async def post(self):
        req = json.loads(self.request.body)
        db_filter = {"name": req["name"]}
        try:
            await self.do_create_one(name="department", req=req, db_filter=db_filter)
        except ValidationError:
            self.write({"error": "unable to add new department"})
            self.set_status(409)
        else:
            self.set_status(201)
            self.write({"department added": req})

    def options(self):
        self.set_status(204)
        self.finish()


class DepartmentHandler(BaseHandler):
    """Department Endpoint."""

    async def get(self, object_id):
        """Get a single department."""
        department = await self.do_find_one(name="department", object_id=object_id)
        self.write({"department": department})

    async def put(self, object_id):
        """Update a single department."""
        req = json.loads(self.request.body)
        try:
            await self.do_update_one(name="department", req=req, object_id=object_id)
        except TypeError:
            self.set_status(404)
            self.write({"error": "cannot find existing department"})
        else:
            self.set_status(200)
            self.write({"department": req})

    async def delete(self, object_id):
        """Delete a single department."""
        try:
            await self.do_delete_one(name="department", object_id=object_id)
        except AttributeError:
            self.set_status(404)
            self.write({"error": "could not delete item"})
        else:
            self.set_status(204)

    def options(self, _):
        self.set_status(204)
        self.finish()


class DepartmentEmployeesHandler(BaseHandler):
    async def get(self, department_id):
        employees = await self.do_populate_many(
            "department", department_id, "employees"
        )
        self.write({"employees": employees})

    def options(self, _):
        self.set_status(204)
        self.finish()


class DepartmentProjectsHandler(BaseHandler):
    async def get(self, department_id):
        projects = await self.do_populate_many("department", department_id, "projects")
        self.write({"projects": projects})

    def options(self, _):
        self.set_status(204)
        self.finish()


class DepartmentAddEmployeeHandler(BaseHandler):
    async def patch(self, department_id, employee_id):
        names = ["department", "employee"]
        fields = ["employees", "department"]
        objects = [department_id, employee_id]
        await self.do_create_list_and_reference(names, fields, objects)
        self.set_status(200)

    def options(self, _, __):
        self.set_status(204)
        self.finish()


class DepartmentAddProjectHandler(BaseHandler):
    async def patch(self, department_id, project_id):
        names = ["department", "project"]
        fields = ["projects", "department"]
        objects = [department_id, project_id]
        await self.do_create_list_and_reference(names, fields, objects)
        self.set_status(200)

    def options(self, _, __):
        self.set_status(204)
        self.finish()
