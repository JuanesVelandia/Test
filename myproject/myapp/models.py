from django.db import models

def custom_upload_to(instance, filename):
    pass

class Archivo(models.Model):
    archivo = models.FileField(upload_to='archivos/')

    # Método para obtener el nombre de archivo deseado
    def get_file_name(self):
        return self.archivo.name.split('/')[-1]


