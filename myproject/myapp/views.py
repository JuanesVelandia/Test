from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArchivoForm
from .models import Archivo
import os
from .tasks import procesar_archivos, resumir_archivos
from django.http import HttpResponse
import mimetypes
import re

def descargar_archivo(request, archivo_id):
    archivo = get_object_or_404(Archivo, pk=archivo_id)
    file_path = archivo.archivo.path

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mimetypes.guess_type(file_path)[0])
            name = re.search(r'[^/]+$', archivo.archivo.name).group(0)
            response['Content-Disposition'] = f'attachment; filename="{name}"'
            return response

    return HttpResponse('El archivo no existe.', status=404)


def borrar_registros(request):
    # Delete all the registers in the database
    Archivo.objects.all().delete()
    
    archivos_dir = './archivos' 
    for archivo in os.listdir(archivos_dir):
        archivo_path = os.path.join(archivos_dir, archivo)
        if os.path.isfile(archivo_path):
            os.remove(archivo_path)

    
    # Redirect the user to the home pafe
    return redirect('subir_archivo')


def subir_archivo(request):

    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save()
            temperatura = request.POST['temperature']  # Get the temperature
            [resultado_procesar,url1,url2,url3,name1,name2,name3] = procesar_archivos(temperatura) 
            summary =  resumir_archivos(temperatura)
            return render(request, 'sucess.html', {'archivo': archivo, 'resultado_procesar': resultado_procesar, 'url1': url1, 'url2': url2, 'url3': url3,'name1': name1,'name2': name2,'name3': name3, 'summary':summary})
        
    else:
        form = ArchivoForm()
    return render(request, 'index.html', {'form': form})


def information(request):
    return render(request, 'info.html')