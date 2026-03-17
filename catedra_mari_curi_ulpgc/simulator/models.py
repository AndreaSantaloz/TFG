from django.db import models




# Posible clase para datos de usuario básicos
class data_user(models.Model):
    id_user=models.BigIntegerField()
    user_name  =models.TextField()
    email = models.EmailField()
    social_media= models.TextField(max_length=100,null=True,blank=True,default='')
    phone= models.TextField()

#Modificar esta clase
class profile_user(models.Model):
    id_user=models.BigIntegerField()
    image = models.ImageField()
    description= models.TextField()
    researchs= models.TextField()
    
# Clase para almacenar modelos de ia
class storage_model(models.Model):
    id_user=models.BigIntegerField()
    