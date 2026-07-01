from django.db import models
from django.contrib.auth.models import User

class Profile_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aboutuser = models.CharField(max_length=500,blank=True, null=True)
    researchs = models.CharField(max_length=1500,blank=True, null=True)
    institution = models.CharField(max_length=255)
    researchfield = models.CharField(max_length=255)
    researcharea = models.CharField(max_length=255)