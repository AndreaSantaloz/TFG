from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_view,name="login"),
    path('sign_up/',views.sign_up_view,name="sign_up"),
    path('sign_up_academic_information/',views.sign_up_academic_view,name="sign_up_academic"),
    path('delete_acount/',views.delete_acount_view,name="delete_acount"),
    path('recover_password/',views.recover_password_view,name="recover_password"),
    path('change_password/',views.change_password_view,name="change_password"),
    path('logout/',views.logout_view,name="logout"),
    path('profile/',views.user_profile,name="user_profile"),
    path('settings/',views.settings,name="settings"),
    path('account_settings/',views.account_settings,name="account_settings"),
    path('accesibility_settings/',views.accesibility_settings,name="accesibility_settings"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
  

]
