from django.shortcuts import render

def index(request):
    return render(request,'base.html',{})

def about_this_app(request):
    return render(request,'base.html',{})
def tutorial(request):
    return render(request,'base.html',{})
