from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('',views.about_this_app,name="about_this_app"),
    path('tutorial/',views.tutorial,name="tutorial"),
    path('',include('user_manager.urls')),
    path('',include('simulator.urls')),
    path('',include('storage.urls')),
   
  
  

]
