from django.db import models
from django.contrib.auth.models import User

class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modelos')
    name = models.CharField(max_length=20)
    file = models.FileField()
    first_date = models.DateField()
    last_date = models.DateField()