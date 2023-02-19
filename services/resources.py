from .models import *
from django.contrib.auth.models import User
from import_export import resources,fields,widgets
class DepartmentResource(resources.ModelResource):

    class Meta:
        model = Department

class ApplicationResource(resources.ModelResource):
    user = fields.Field(
        column_name='Username',
        attribute='user',
        widget=widgets.ForeignKeyWidget(User, 'username'))
    class Meta:
        model = Application
        fields = ['user','department_preferences','linkedin_url','instagram_id','lookup_skills','question_one','question_two' ,'status','date_of_application']