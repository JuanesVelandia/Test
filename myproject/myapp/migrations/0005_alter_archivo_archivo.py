# Generated by Django 4.2.5 on 2023-09-10 15:31

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_archivo_nombre_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='archivo',
            field=models.FileField(upload_to=myapp.models.custom_upload_to),
        ),
    ]
