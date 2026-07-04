from pathlib import Path

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import get_valid_filename


def user_model_upload_path(instance, filename):
    safe_filename = get_valid_filename(Path(filename).name)
    return f"models/user_{instance.user_id}/{safe_filename}"

class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modelos')
    name = models.CharField(max_length=20)
    file = models.FileField(upload_to=user_model_upload_path)
    first_date = models.DateField()
    last_date = models.DateField()
