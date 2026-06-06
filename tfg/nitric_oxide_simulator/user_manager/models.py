from django.db import models
from django.contrib.auth.models import User

class Profile_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    researchfield = models.CharField(max_length=255)
    researcharea = models.CharField(max_length=255)