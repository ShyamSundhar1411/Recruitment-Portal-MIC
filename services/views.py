from .models import *
from django.shortcuts import render

# Create your views here.
def home(request):
    recruitment_drives = RecruitmentDrive.objects.all().order_by('-start_date_time')
    return render(request,'services/home.html',{"Recruitment_Drives":recruitment_drives})
