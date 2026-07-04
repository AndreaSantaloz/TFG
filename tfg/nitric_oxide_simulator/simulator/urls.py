
from django.urls import include, path
from . import views


urlpatterns = [
    path('home/',views.home,name="home"),
    path('simulator/',views.simulator,name="simulator"),
    path('save_model/',views.save_model,name="save_model"),
    path('stop_model/',views.stop_model,name="stop_model"),
    
]
