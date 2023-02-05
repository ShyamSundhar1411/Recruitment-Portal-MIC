import datetime
from .tasks import *
from .models import *
from .forms import *
from .mixins import *
from .filters import *
from .resources import *
from dal import autocomplete
from taggit.models import Tag
from .aiding_functions import *
from django.views import generic
from django.contrib import messages
from django.http import Http404, JsonResponse,HttpResponse
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required,user_passes_test


# Create your views here.
#Class Based Views
# AutoComplete Class Based View
class UsersAutoComplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(username__icontains=self.q)
        return qs
class TagsAutoComplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

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
class ApplicationUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Application
    fields = ["department_preferences","tags","linkedin_url","question_one","question_two"]
    template_name = "services/UpdateApplication.html"
    context_object_name = "application"
    
    def get_object(self):
        application_form = super(ApplicationUpdateView,self).get_object()
        if self.request.user == application_form.user:
            return application_form
        raise Http404
    def get_success_url(self):
        slug = self.kwargs['slug']
        messages.success(self.request,'Updated Successfully')
        return reverse("update_application", kwargs={"slug": slug})
#Funciton Based Views
def landing_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request,"services/landing_page.html")
@login_required
def home(request):
    user_status = is_authorized(request.user)
    today = datetime.datetime.now()
    if request.user.profile.role == "Unauthorized" or request.user.profile.contact == "None":
        messages.info(request,"Verify your account by adding in your contact.")
        return redirect("profile",request.user.profile.slug)
    recruitment_drives = RecruitmentDrive.objects.all().order_by('-start_date_time')
    applications = Application.objects.filter(user = request.user).order_by('-date_of_application')
    return render(request,'services/home.html',{"Recruitment_Drives":recruitment_drives,"Status":user_status,"Applications":applications,})
@login_required
def submit_application(request,slug):
    recruitment_drive = RecruitmentDrive.objects.get(slug = slug)
    if Application.objects.filter(user = request.user,recruitment_drive = recruitment_drive).exists():
        messages.info(request,"You have already queued an application for this recruitment drive. Kindly Wait till your application is reviewed.")
        return redirect("home")
    if request.method == "POST":
        recruitment_form = RecruitmentForm(request.POST)
        if recruitment_form.is_valid():
            recruitment = recruitment_form.save(commit=False)
            recruitment.user = request.user
            recruitment.status = "Application under Review"
            recruitment.lookup_skills = list_to_string_converter(recruitment_form.cleaned_data['tags'])
            recruitment.recruitment_drive = recruitment_drive
            recruitment.save()
            recruitment_form.save_m2m()
            application_confirmation_mail(request.user)
            messages.success(request,"Successfully submitted Application. You will be notified about the status soon")
            return redirect("home")
        else:
            return render(request,"services/recruitment_application.html",{"form":recruitment_form,"hostride_form_errors":recruitment_form.errors,"drive":recruitment_drive})
    else:
        return render(request,"services/recruitment_application.html",{"form":RecruitmentForm(),"drive":recruitment_drive})
@login_required
@user_passes_test(lambda user:is_authorized(user))
def view_all_applications(request):
    applications = ApplicationFilter(request.GET,queryset = Application.objects.all())
    request.session['query_set'] = [application.id for application in applications.qs]
    return render(request,'services/view_all_applications.html',{"filterer":applications,"form_choices":FORM_STATUS_CHOICES})
@login_required
@user_passes_test(lambda user:is_authorized(user))
def delete_recruitment_drive(request,pk,slug):
    if request.method == "POST":
        recruitment_drive = RecruitmentDrive.objects.get(pk=pk,slug = slug)
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

@login_required
def generate_csv(request):
    application_resource = ApplicationResource()
    queryset = [Application.objects.get(id=id) for id in request.session['query_set']]
    dataset = application_resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications{}.csv"'.format(datetime.datetime.now())
    return response
@login_required
@user_passes_test(lambda user:is_authorized(user))
def update_application_status(request,slug,pk):
    application = Application.objects.get(slug = slug,pk = pk)
    if request.method == "POST":
        status = str(request.POST['status_selector'])
        application.status = status
        application.save()
        if status == "Shortlisted for Interview":
            shortlist_mail(application.user)
        elif status == "Accepted":
            acceptance_mail(application.user)
        elif status == "Mentorship":
            mentorship_mail(application.user)
        else:
            pass
        messages.success(request,"Successfully Updated Status of application {}".format(application.slug))
        return redirect("view_all_applications")