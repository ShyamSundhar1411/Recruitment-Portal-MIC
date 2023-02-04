from .models import *
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
class DepartmentResource(resources.ModelResource):

    class Meta:
        model = Department
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
# Register your models here.
admin.site.register(RecruitmentDrive)
admin.site.register(Profile)
admin.site.register(Application)
admin.site.register(Department,DepartmentAdmin)
