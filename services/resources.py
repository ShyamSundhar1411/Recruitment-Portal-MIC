from .models import *
from import_export import resources
class DepartmentResource(resources.ModelResource):

    class Meta:
        model = Department
class ApplicationResource(resources.ModelResource):

    class Meta:
        model = Application