
from django.db import models
from django.contrib.auth.models import User

"""
PERFIL DE USUARIO
"""
class ProfileUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name = 'profile',
    )
    institution= models.CharField(max_length=255)
    orcid = models.CharField(max_length=19,unique=True)
    areas_of_specialization=models.TextField()
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    abstract_personal=models.TextField(blank=True,null=True)
    github=models.CharField(max_length=200,blank=True,null=True)

""" 
MODELO DE USUARIO
"""   

class UserModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'model',
    )
    filename = models.CharField(max_length=255)
    usermodel_url = models.URLField(blank=True,null=True)
    extension= models.CharField(max_length=10)
    size=models.BigIntegerField()
    upload_date=models.DateTimeField(auto_now_add=True)
    last_access=models.DateTimeField(auto_now=True)

"""
REGISTRO DE SIMULACION DEL USUARIO
"""
class Simulation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'simulation',
    )
    first_access=models.DateField()
    last_access=models.DateField()
    duration = models.TimeField()
    
