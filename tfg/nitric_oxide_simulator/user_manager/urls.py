from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_view,name="login"),
    path('sign_up/',views.sign_up_view,name="sign_up"),
    path('sign_up_academic_information/',views.sign_up_academic_view,name="sign_up_academic"),
    path('logout/',views.logout_view,name="logout"),
    path('profile/',views.user_profile,name="user_profile"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
  

]
