from django.apps import AppConfig

class MyappConfig(AppConfig):
    # Configuration class for the 'myapp' Django app.

    # Define the default auto field for models (used for migrations).
    default_auto_field = 'django.db.models.BigAutoField'

    # Set the name of the app.
    name = 'myapp'
