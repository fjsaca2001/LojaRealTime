# Generated by Django 3.2.4 on 2022-10-19 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0004_remove_vehiculos_ubicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculos',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]