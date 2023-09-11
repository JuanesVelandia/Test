from django.urls import path
from . import views

urlpatterns = [
    path('', views.subir_archivo, name='subir_archivo'),
    path('descargar/<int:archivo_id>/', views.descargar_archivo, name='descargar_archivo'),
    path('borrar_registros/', views.borrar_registros, name='borrar_registros'),
    path('information/', views.information ,name="information")
]
