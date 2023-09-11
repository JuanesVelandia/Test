from django import forms
from .models import Archivo
import os

# Custom validation function to check if the file extension is valid
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

    # Get the file extension from the uploaded file
    file_extension = os.path.splitext(value.name)[1]

    # Check if the file extension is in the list of valid extensions
    if file_extension.lower() not in valid_extensions:
        raise forms.ValidationError("The file extension is not valid")

# Define a form for uploading files associated with the 'Archivo' model
class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ['archivo']

    archivo = forms.FileField(
        validators=[validate_file_extension],  # Apply the custom validation
        label='Upload your programming language code file',
        help_text=''
    )
