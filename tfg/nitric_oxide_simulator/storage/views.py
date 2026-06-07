from django.shortcuts import render
from .models import UserModel
# Create your views here.
def storage_view(request):
    lista = UserModel.objects.filter(user=request.user)
    return render(request,'storage/storage.html',{'lista':lista})

    