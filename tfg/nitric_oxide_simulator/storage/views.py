from django.shortcuts import render
from .models import UserModel
def storage_view(request):
    lista = UserModel.objects.filter(user=request.user)
    return render(request,'storage/storage.html',{'lista':lista})

    