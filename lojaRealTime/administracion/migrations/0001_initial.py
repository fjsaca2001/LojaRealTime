# Generated by Django 3.2.4 on 2022-09-27 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_usuario', models.CharField(max_length=30)),
                ('id_vehiculo', models.CharField(max_length=30)),
                ('latitud', models.CharField(max_length=30)),
                ('longitud', models.CharField(max_length=30)),
                ('fecha_hora', models.CharField(max_length=30)),
                ('altitud', models.CharField(max_length=30)),
                ('velocidad', models.CharField(max_length=30)),
                ('acuri', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=30)),
                ('gps', models.CharField(max_length=30)),
                ('conexion', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=30)),
                ('temperatura', models.CharField(max_length=30)),
                ('consumo', models.CharField(max_length=30)),
                ('red', models.CharField(max_length=30)),
                ('bateria', models.CharField(max_length=30)),
                ('hora_actual', models.CharField(max_length=30)),
            ],
        ),
    ]