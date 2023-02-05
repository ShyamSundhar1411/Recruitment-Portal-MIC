from .models import *
from .forms import *
from .mixins import *
from .aiding_functions import *
from django.views import generic
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.
class RecruitmentDriveUpdateView(LoginRequiredMixin,AuthorizationMixin,generic.UpdateView):
    model = RecruitmentDrive
    fields = ["recruitment_title","recruitment_term","department","status","start_date_time","end_date_time"]
    template_name = "services/UpdateRecruitmentDrive.html"
    context_object_name = "recruitment_drive"
    
    def get_object(self):
        recruitment_drive = super(RecruitmentDriveUpdateView,self).get_object()
        if not is_authorized(self.request.user) :
            raise Http404
        return recruitment_drive
    def get_success_url(self):
        pk = self.kwargs["pk"]
        messages.success(self.request,'Updated Successfully')
        return reverse("update_recruitment", kwargs={"pk": pk})
#Funciton Based Views
def home(request):
    user_status = is_authorized(request.user)
    recruitment_drives = RecruitmentDrive.objects.all().order_by('-start_date_time')
    return render(request,'services/home.html',{"Recruitment_Drives":recruitment_drives,"Status":user_status})
@login_required
def delete_recruitment_drive(request,pk):
    if request.method == "POST":
        recruitment_drive = RecruitmentDrive.objects.get(pk=pk)
        recruitment_drive.delete()
        messages.success(request,"Operation Successful")
        return redirect("home")
    else:
        messages.error(request,"Error Processing Request")
        return redirect("home")
@login_required
def profile(request,slug):
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance = request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            if request.user.profile.department == None:
                profile_form_copy = profile_form.save(commit = False)
                if email_checker(request.user.email):
                    profile_form_copy.role = 'Applicant'
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
            return redirect('home')
        else:
            return render(request, 'account/profile.html', {'user_form':user_form,'profile_form':profile_form,'user_form_errors':user_form.errors,'profile_form_errors':profile_form.errors})
    else:
        user_form = UserForm(instance = request.user)
        profile_form = ProfileForm(instance = request.user.profile)
        return render(request,'account/profile.html',{'user_form':user_form,'profile_form':profile_form})