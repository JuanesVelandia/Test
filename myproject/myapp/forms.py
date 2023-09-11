from django import forms
from .models import Archivo
import os

# Función de validación personalizada para verificar la extensión del archivo
def validate_file_extension(value):
    valid_extensions = [
        ".c", ".cpp", ".h", ".hpp",
        ".java", ".class", ".jar",
        ".py", ".pyc", ".pyo", ".pyw",
        ".js",
        ".html", ".htm",
        ".css",
        ".rb",
        ".php",
        ".pl", ".pm",
        ".swift",
        ".go",
        ".kt",
        ".rs",
        ".ts",
        ".sql",
        ".json",
        ".xml",
        ".yaml", ".yml",
        ".sh",
        ".bat", ".cmd",
        ".md",
        ".dart",
        ".scala",
        ".hs",
        ".lua",
        ".r",
        ".m",
        ".groovy",
        ".cbl",
        ".f", ".f90"
    ]
    file_extension = os.path.splitext(value.name)[1]  # Obtiene la extensión del archivo
    if file_extension.lower() not in valid_extensions:
        raise forms.ValidationError("The file extension is not valid")

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ['archivo']

    archivo = forms.FileField(
        validators=[validate_file_extension],
        label='Upload your programming language code file',
        help_text=''
    )

