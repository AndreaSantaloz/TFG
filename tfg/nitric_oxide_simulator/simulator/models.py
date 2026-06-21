from django.db import models
from storage.models import UserModel
from django.contrib.auth.models import User

class User_simulation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    model = UserModel()
    first_date = models.DateField()
    last_date = models.DateField()
