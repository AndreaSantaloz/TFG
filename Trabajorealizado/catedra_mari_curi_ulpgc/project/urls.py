"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Trabajorealizado.catedra_mari_curi_ulpgc.simulator import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #Página principal
    path('',views.index,name="index" ),
    #Paginas asociadas a la principal
    path('about_this_app/',views.about_this_app,name="about_this_app" ),
    path('help/',views.help,name="help" ),
    path('privacy_terms/',views.privacy_terms,name="privacy_terms" ),
    #Autenticación
    path('login/',views.login_view,name="login" ),
    path('sign_up/',views.sign_up,name="sign_up" ),
    #Perfil
    path('profile/',views.profile,name="profile" ),
    #Almacenamiento
    path('store/',views.store,name="store" ),
    path('add_model/',views.add_model,name="add_model" ),
    path('delete_model/',views.delete_model,name="delete_model" ),
    #tutorial
    path('tutorial/',views.tutorial,name="tutorial" ),
    #Ajustes
    path('setting/',views.setting,name="setting" ),
    path('recover_password/',views.recover_password,name="recover_password" ),
    path('change_password/',views.change_password,name="change_password" ),
    path('delete_account/',views.delete_account,name="delete_account" ),
    path('edit_profile/',views.edit_profile,name="edit_profile" ),
    #Simulador
    path('home/',views.home,name="home" ),
    path('checking_inputs/',views.checking_inputs,name="checking_inputs" ),
    path('simulator/',views.simulator,name="simulator" ),
    path('exit/',views.exit,name="exit"),
    path('admin/', admin.site.urls),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
