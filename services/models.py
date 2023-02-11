import uuid
import shortuuid
from .choices import *
from django.db import models
from django.dispatch import receiver
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length = 100)
    department_id = models.CharField(max_length = 100)
    department_school = models.CharField(max_length = 100,choices = SCHOOL_CHOICES)
    def __str__(self):
        return self.department_name
    
class RecruitmentDrive(models.Model):
    recruitment_title = models.CharField(max_length = 200)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    recruitment_term = models.CharField(max_length = 500)
    status = models.CharField(max_length = 100,choices = RECRUITMENT_STATUS_CHOICES)
    department = models.CharField(max_length = 100,choices = DRIVE_DEPARTMENT_CHOICES,default = "All")
    slug = models.SlugField(blank = True)
    def __str__(self):
        return self.recruitment_title+'-'+self.department
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super(RecruitmentDrive, self).save(*args,**kwargs)
class Application(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recruitment_drive = models.ForeignKey(RecruitmentDrive,on_delete=models.CASCADE)
    department_preferences = MultiSelectField(choices=DEPARTMENT_CHOICES,max_choices=2,max_length = 100)
    linkedin_url = models.URLField(max_length = 200)
    instagram_id = models.CharField(max_length = 100)
    lookup_skills = models.CharField(max_length = 400)
    question_one = models.TextField(max_length = 1000)
    question_two = models.TextField(max_length = 1000,blank = True)
    status = models.CharField(max_length = 100,choices = STATUS_CHOICES)
    tags = TaggableManager()
    slug = models.SlugField(blank = True)
    date_of_application = models.DateTimeField(auto_now = True)
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = shortuuid.ShortUUID().random(length=10)
        super(Application, self).save(*args,**kwargs)
    def __str__(self):
        return self.user.username+"-"+self.recruitment_drive.recruitment_term


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = PhoneNumberField(blank = True)
    role = models.CharField(max_length = 100,choices = ROLE_CHOICES,blank = True, null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null = True)
    admitted_year = models.CharField(max_length = 500,null=True)
    slug = models.SlugField(blank=True)
    def __str__(self):
        return self.user.username
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super(Profile, self).save(*args,**kwargs)
@receiver(post_save,sender = User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user = instance,role = "Unauthorized",department = None)
        instance.profile.save()
@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()