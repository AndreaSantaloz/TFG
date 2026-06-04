from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'simulator/home.html',{})
def data_definition(request):
    return render(request,'simulator/data_definition.html',{})
def simulator(request):
    return render(request,'simulator/simulator.html',{})
def temporal_history(request):
    return render(request,'simulator/temporal_history.html',{})