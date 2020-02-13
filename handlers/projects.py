import json
from marshmallow.exceptions import ValidationError
from handlers.base import BaseHandler


class ProjectsHandler(BaseHandler):
    """Projects Endpoint."""

    async def get(self):
        projects = await self.do_find(name="project")
        self.write({"projects": projects})

    async def post(self):
        req = json.loads(self.request.body)
        db_filter = {"name": req["name"]}
        try:
            await self.do_create_one(name="project", req=req, db_filter=db_filter)
        except ValidationError:
            self.write({"error": "unable to add new project"})
            self.set_status(409)
        else:
            self.set_status(201)
            self.write({"project added": req})

    def options(self):
        self.set_status(204)
        self.finish()


class ProjectHandler(BaseHandler):
    """project Endpoint."""

    async def get(self, object_id):
        """Get a single project."""
        project = await self.do_find_one(name="project", object_id=object_id)
        self.write({"project": project})

    async def put(self, object_id):
        """Update a single project."""
        req = json.loads(self.request.body)
        try:
            await self.do_update_one(name="project", req=req, object_id=object_id)
        except TypeError:
            self.set_status(404)
            self.write({"error": "cannot find existing project"})
        else:
            self.set_status(200)
            self.write({"project": req})

    async def delete(self, object_id):
        """Delete a single project."""
        try:
            await self.do_delete_one(name="project", object_id=object_id)
        except AttributeError:
            self.set_status(404)
            self.write({"error": "could not delete item"})
        else:
            self.set_status(204)

    def options(self, _):
        self.set_status(204)
        self.finish()


class ProjectEmployeesHandler(BaseHandler):
    async def get(self, project_id):
        employees = await self.do_populate_many("project", project_id, "employees")
        self.write({"employees": employees})

    def options(self, _):
        self.set_status(204)
        self.finish()


class ProjectDepartmentsHandler(BaseHandler):
    async def get(self, project_id):
        try:
            department = await self.do_populate_one("project", project_id, "department")
        except:
            self.write({"department": None})
        else:
            self.write({"department": department})


class ProjectAddEmployeeHandler(BaseHandler):
    async def patch(self, project_id, employee_id):
        names = ["project", "employee"]
        fields = ["employees", "projects"]
        objects = [project_id, employee_id]
        await self.do_create_relation(names, fields, objects)

    def options(self, _, __):
        self.set_status(204)
        self.finish()


class ProjectAddDepartmentHandler(BaseHandler):
    async def patch(self, project_id, department_id):
        names = ["department", "project"]
        fields = ["projects", "department"]
        objects = [department_id, project_id]
        await self.do_create_list_and_reference(names, fields, objects)
        self.set_status(200)

    def options(self, _, __):
        self.set_status(204)
        self.finish()
