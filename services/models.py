import uuid
from .choices import *
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save
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
    end_data_time = models.DateTimeField()
    recruitment_term = models.CharField(max_length = 500)
    
    def __str__(self):
        return self.recruitment_title+'-'+self.recruitment_term
class Application(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recruitment_drive = models.ForeignKey(RecruitmentDrive,on_delete=models.CASCADE)
    deparment_one = models.CharField(max_length = 100)
    department_two = models.CharField(max_length = 200)
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