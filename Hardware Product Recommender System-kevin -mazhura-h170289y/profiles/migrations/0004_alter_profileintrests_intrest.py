# Generated by Django 4.0.3 on 2022-05-25 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_product_link'),
        ('profiles', '0003_profileintrests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileintrests',
            name='intrest',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.category'),
            preserve_default=False,
        ),
    ]
