
from django.urls import include, path
from . import views


urlpatterns = [
    path('home/',views.home,name="home"),
    path('data_definition/',views.data_definition,name="data_definition"),
    path('simulator/',views.simulator,name="simulator"),
    path('temporal_history/',views.temporal_history,name="temporal_history"),

]
