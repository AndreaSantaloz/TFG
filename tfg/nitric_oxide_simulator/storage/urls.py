
from django.urls import include, path
from . import views


urlpatterns = [
    path('storage/',views.storage_view,name="storage"),
    path('add_model/',views.add_model,name="add_model"),
    path('delete_model/',views.delete_model,name="delete_model"),
    path('simulate_model/',views.simulate_model,name="simulate_model"),
   

]
