from django.shortcuts import render

# Create your views here.
def storage_view(request):
    return render(request,'storage/storage.html',{})