from .models import *
from .resources import *
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource

class ApplicationAdmin(ImportExportModelAdmin):
    resource_class = ApplicationResource
# Register your models here.
admin.site.register(RecruitmentDrive)
admin.site.register(Profile)
admin.site.register(Application,ApplicationAdmin)
admin.site.register(Department,DepartmentAdmin)

