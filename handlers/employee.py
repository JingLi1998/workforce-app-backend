import json
from marshmallow.exceptions import ValidationError
from handlers.base import BaseHandler


class EmployeesHandler(BaseHandler):
    """Employees Endpoint."""

    async def get(self):
        employees = await self.do_find(name="employee")
        self.write({"employees": employees})

    async def post(self):
        req = json.loads(self.request.body)
        db_filter = {"salary_id": req["salary_id"]}
        try:
            await self.do_create_one(name="employee", req=req, db_filter=db_filter)
        except ValidationError:
            self.write({"error": "unable to add new employee"})
            self.set_status(409)
        else:
            self.set_status(201)
            self.write({"employee added": req})

    def options(self):
        self.set_status(204)
        self.finish()


class EmployeeHandler(BaseHandler):
    """Employee Endpoint."""

    async def get(self, object_id):
        """Get a single employee."""
        employee = await self.do_find_one(name="employee", object_id=object_id)
        self.write({"employee": employee})

    async def put(self, object_id):
        """Update a single employee."""
        req = json.loads(self.request.body)
        try:
            await self.do_update_one(name="employee", req=req, object_id=object_id)
        except TypeError:
            self.set_status(404)
            self.write({"error": "cannot find existing employee"})
        else:
            self.set_status(200)
            self.write({"employee": req})

    async def delete(self, object_id):
        """Delete a single employee."""
        try:
            await self.do_delete_one(name="employee", object_id=object_id)
        except AttributeError:
            self.set_status(404)
            self.write({"error": "could not delete item"})
        else:
            self.set_status(204)

    def options(self, _):
        self.set_status(204)
        self.finish()


class EmployeeDepartmentsHandler(BaseHandler):
    async def get(self, employee_id):
        try:
            department = await self.do_populate_one(
                "employee", employee_id, "department"
            )
        except:
            self.write({"department": None})
        else:
            self.write({"department": department})

    def options(self, _):
        self.set_status(204)
        self.finish()


class EmployeeProjectsHandler(BaseHandler):
    async def get(self, employee_id):
        projects = await self.do_populate_many("employee", employee_id, "projects")
        self.write({"projects": projects})

    def options(self, _):
        self.set_status(204)
        self.finish()


class EmployeeAddDepartmentHandler(BaseHandler):
    async def patch(self, employee_id, department_id):
        names = ["department", "employee"]
        fields = ["employees", "department"]
        objects = [department_id, employee_id]
        await self.do_create_list_and_reference(names, fields, objects)
        self.set_status(200)

    def options(self, _, __):
        self.set_status(204)
        self.finish()


class EmployeeAddProjectHandler(BaseHandler):
    async def patch(self, employee_id, project_id):
        names = ["employee", "project"]
        fields = ["projects", "employees"]
        objects = [employee_id, project_id]
        await self.do_create_relation(names, fields, objects)

    def options(self, _, __):
        self.set_status(204)
        self.finish()
