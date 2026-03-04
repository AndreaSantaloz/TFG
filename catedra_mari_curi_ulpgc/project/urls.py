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
from simulator import views

urlpatterns = [
    path('',views.index,name="index" ),
    path('login/',views.login,name="login" ),
    path('sign_up/',views.sign_up,name="sign_up" ),
    path('simulator/',views.simulator,name="simulator" ),
    
    path('profile/',views.profile,name="profile" ),
    path('store/',views.store,name="store" ),
    path('setting/',views.setting,name="setting" ),
    path('upload_model/',views.upload_model,name="upload_model" ),
    path('tabular_chart/',views.tabular_chart,name="tabular_chart" ),
    path('dispersion_charts/',views.dispersion_chart,name="dispersion_chart" ),
    path('correlation_charts/',views.correlation_chart,name="correlation_chart" ),
    path('erros_charts/',views.errors_chart,name="erros_chart" ),
    path('volume_charts/',views.volume_chart,name="volume_charts" ),


    
    
    
    path('admin/', admin.site.urls),
]
