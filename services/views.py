from .models import *
from .forms import *

from .aiding_functions import *
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    user_status = is_authorized(request.user)
    recruitment_drives = RecruitmentDrive.objects.all().order_by('-start_date_time')
    return render(request,'services/home.html',{"Recruitment_Drives":recruitment_drives,"Status":user_status})
@login_required
def profile(request,slug):
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance = request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            if request.user.profile.department == None:
                profile_form_copy = profile_form.save(commit = False)
                if email_checker(request.user.email):
                    profile_form_copy.role = 'Student'
                    department = Department.objects.get(department_id = department_finder(request.user.last_name))
                    admitted_year = admitted_year_finder(request.user.last_name)
                    profile_form_copy.department = department
                    profile_form_copy.admitted_year = admitted_year
                else:
                    profile_form_copy.role = 'Unauthorized'
                    profile_form_copy.department = Department.objects.get(department_name = "Unauthorized")
                user_form.save()
                profile_form_copy.save()
            else:
                user_form.save()
                profile_form.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('profile',slug = request.user.profile.slug)
        else:
            return render(request, 'account/profile.html', {'user_form':user_form,'profile_form':profile_form,'user_form_errors':user_form.errors,'profile_form_errors':profile_form.errors})
    else:
        user_form = UserForm(instance = request.user)
        profile_form = ProfileForm(instance = request.user.profile)
        return render(request,'account/profile.html',{'user_form':user_form,'profile_form':profile_form})