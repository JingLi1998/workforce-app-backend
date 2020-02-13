from handlers.employee import (
    EmployeesHandler,
    EmployeeHandler,
    EmployeeDepartmentsHandler,
    EmployeeProjectsHandler,
    EmployeeAddDepartmentHandler,
    EmployeeAddProjectHandler,
)
from handlers.department import (
    DepartmentsHandler,
    DepartmentHandler,
    DepartmentEmployeesHandler,
    DepartmentProjectsHandler,
    DepartmentAddEmployeeHandler,
    DepartmentAddProjectHandler,
)
from handlers.projects import (
    ProjectsHandler,
    ProjectHandler,
    ProjectEmployeesHandler,
    ProjectDepartmentsHandler,
    ProjectAddEmployeeHandler,
    ProjectAddDepartmentHandler,
)

url_patterns = [
    ("/api/employees[/]?", EmployeesHandler),
    ("/api/employees/([^/]+)[/]?", EmployeeHandler),
    ("/api/employees/([^/]+)/departments[/]?", EmployeeDepartmentsHandler),
    ("/api/employees/([^/]+)/projects[/]?", EmployeeProjectsHandler),
    ("/api/employees/([^/]+)/departments/([^/]+)[/]?", EmployeeAddDepartmentHandler),
    ("/api/employees/([^/]+)/projects/([^/]+)[/]?", EmployeeAddProjectHandler),
    ("/api/departments[/]?", DepartmentsHandler),
    ("/api/departments/([^/]+)[/]?", DepartmentHandler),
    ("/api/departments/([^/]+)/projects[/]?", DepartmentProjectsHandler),
    ("/api/departments/([^/]+)/employees[/]?", DepartmentEmployeesHandler),
    ("/api/departments/([^/]+)/employees/([^/]+)[/]?", DepartmentAddEmployeeHandler),
    ("/api/departments/([^/]+)/projects/([^/]+)[/]?", DepartmentAddProjectHandler),
    ("/api/projects[/]?", ProjectsHandler),
    ("/api/projects/([^/]+)[/]?", ProjectHandler),
    ("/api/projects/([^/]+)/employees[/]?", ProjectEmployeesHandler),
    ("/api/projects/([^/]+)/departments[/]?", ProjectDepartmentsHandler),
    ("/api/projects/([^/]+)/employees/([^/]+)[/]?", ProjectAddEmployeeHandler),
    ("/api/projects/([^/]+)/departments/([^/]+)[/]?", ProjectAddDepartmentHandler),
]
