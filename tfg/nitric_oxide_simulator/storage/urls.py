
from django.urls import include, path
from . import views


urlpatterns = [
    path('storage/',views.storage_view,name="storage"),
   

]
