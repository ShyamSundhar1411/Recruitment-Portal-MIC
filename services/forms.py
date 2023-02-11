from . models import *
from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from taggit.forms import *
class RecruitmentForm(forms.ModelForm):
    question_one = forms.CharField(label = "Why do you want to apply for MIC ?",help_text = 'Include Previous Works as well',widget = forms.Textarea)
    question_two = forms.CharField(label = "How did you hear about MIC ?",required = False,widget = forms.Textarea)
    tags = TagField(label = "Skills",help_text = "Add Skills as comma seperated Values")
    class Meta:
        model = Application
        fields = ['department_preferences','linkedin_url','tags','question_one','question_two','instagram_id']
        widgets = {
            'tags' :TagWidget(attrs={'data-role':'tagsinput','placeholder':'Add Tags','class':'form-control'})
        }
class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    email = forms.CharField(disabled=True)
    first_name = forms.CharField(disabled=True)
    last_name = forms.CharField(disabled=True)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
class ProfileForm(forms.ModelForm):
    contact = PhoneNumberField(required = True)
    role = forms.CharField(disabled=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(),disabled=True,required=False)    
    admitted_year = forms.CharField(disabled=True,required=False) 
    class Meta:
        model = Profile
        fields = ['role','contact','department','admitted_year']