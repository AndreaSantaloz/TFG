from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import UserModel
from django.utils import timezone

def storage_view(request):
    lista = UserModel.objects.filter(user=request.user)
    return render(request,'storage/storage.html',{'lista':lista})


def add_model(request):
    if request.method == "POST" and request.FILES:
        name = request.POST.get('name')
        model = request.FILES.get('model')
        usermodel = UserModel(
                             user = request.user,
                             name = name,
                             file = model,
                             first_date = timezone.now().date(),
                             last_date = timezone.now().date()

        )
        usermodel.save()
        return redirect('storage')

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

def delete_model(request):
    if request.method == "POST":
        id_model = request.POST.get('id_eliminar')
        
        if id_model:
            modelo = get_object_or_404(UserModel, id=id_model, user=request.user)
            
            if modelo.file:
                modelo.file.delete(save=False)
                
            modelo.delete()
            return redirect('storage') 
            
        return JsonResponse({'success': False, 'message': 'ID no proporcionado'}, status=400)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
 


def simulate_model(request):
    if request.method == "POST":
        id_model = request.POST.get('id_simulator')
        if id_model:
            modelo = get_object_or_404(UserModel, id=id_model, user=request.user)
            request.session['archivo_modelo_id'] = modelo.id
            return redirect('home')
                

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
 




    