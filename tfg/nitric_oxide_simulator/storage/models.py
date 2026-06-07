from django.db import models
from django.contrib.auth.models import User

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    file = models.FileField()
    first_date = models.DateField()
    last_date = models.DateField()