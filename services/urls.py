from django.urls import path,include
from services import views

urlpatterns = [
    path('',views.home,name = "home",),
    path('profile/<slug:slug>/view',views.profile,name = "profile"),
    
    #Recruitment Drive
    path('update/<int:pk>/recruitment/drive/',views.RecruitmentDriveUpdateView.as_view(),name = "update_recruitment"),
    path('delete/<int:pk>/recruitment/drive/<slug:slug>/',views.delete_recruitment_drive,name = "delete_recruitment_drive"),
    
    #Autocompeltes
    path('users/autocomplete/',views.UsersAutoComplete.as_view(),name = "user_autocomplete"),
    path('tags/autocomplete/',views.TagsAutoComplete.as_view(),name = "tags_autocomplete"),
    #Application
    path('application/<slug:slug>/recruitment/term/',views.submit_application,name = "submit_application"),
    path('application/<slug:slug>/edit/',views.ApplicationUpdateView.as_view(),name = "update_application"),
    path('mic/view/applications/<slug:slug>/all',views.view_all_applications,name = "view_all_applications"),
    path('export/application/csv',views.generate_csv,name = "generate_csv"),
    path('update/<slug:slug>/application/<int:pk>/status',views.update_application_status,name = "update_application_status"),
    path('application/send_mass_mail',views.send_mass_mail,name = "send_mass_mail"),
]