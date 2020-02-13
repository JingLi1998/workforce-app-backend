from umongo import MotorTornadoInstance, Document, fields, validate

instance = MotorTornadoInstance()


@instance.register
class Employee(Document):
    salary_id = fields.StringField(
        required=True, validate=validate.Regexp("[m|f|l]\d{6}")
    )
    first_name = fields.StringField(required=True, validate=validate.Regexp("\D+"))
    last_name = fields.StringField(required=True, validate=validate.Regexp("\D+"))
    role = fields.StringField(required=True)
    department = fields.ReferenceField("Department")
    projects = fields.ListField(fields.ReferenceField("Project"))

    class Meta:
        collection_name = "employees"


@instance.register
class Department(Document):
    name = fields.StringField(required=True)
    location = fields.StringField(required=True)
    employees = fields.ListField(fields.ReferenceField("Employee"))
    projects = fields.ListField(fields.ReferenceField("Project"))

    class Meta:
        collection_name = "departments"


@instance.register
class Project(Document):
    name = fields.StringField(required=True)
    description = fields.StringField(required=True)
    department = fields.ReferenceField("Department")
    employees = fields.ListField(fields.ReferenceField("Employee"))

    class Meta:
        collection_name = "projects"


document_templates = {
    "employee": Employee,
    "department": Department,
    "project": Project,
}
