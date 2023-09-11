from django.db import models

# Model representing an uploaded file
class Archivo(models.Model):
    archivo = models.FileField(upload_to='archivos/')

    # Method to get the file name from the file path
    def get_file_name(self):
        return self.archivo.name.split('/')[-1]
