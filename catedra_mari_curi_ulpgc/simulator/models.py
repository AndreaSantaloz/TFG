from django.db import models

# Create your models here.

class profile_user(models.Model):
    id_user=models.BigIntegerField()
    user_name  =models.TextField()
    email = models.EmailField()
    social_media= models.TextField(max_length=100,null=True,blank=True,default='')
    phone= models.TextField()
    image = models.ImageField()
    description= models.TextField()
    researchs= models.TextField()
  
    