# Generated by Django 3.1.14 on 2022-03-09 09:03

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20220309_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinestore',
            name='image',
            field=models.ImageField(null=True, upload_to=app.models.user_directory_path),
        ),
    ]