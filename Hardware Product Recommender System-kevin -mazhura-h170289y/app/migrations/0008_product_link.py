# Generated by Django 4.0.3 on 2022-05-16 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.CharField(max_length=100, null=True),
        ),
    ]