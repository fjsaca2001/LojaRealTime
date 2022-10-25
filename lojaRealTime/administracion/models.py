# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Vehiculos(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.CharField(max_length=30, blank=True, null=True)
    id_vehiculo = models.CharField(max_length=30, blank=True, null=True)
    latitud = models.CharField(max_length=30, blank=True, null=True)
    longitud = models.CharField(max_length=30, blank=True, null=True)
    fecha_hora = models.CharField(max_length=30, blank=True, null=True)
    altitud = models.CharField(max_length=30, blank=True, null=True)
    velocidad = models.IntegerField(blank=True, null=True)
    acuri = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=30, blank=True, null=True)
    gps = models.IntegerField(blank=True, null=True)
    conexion = models.IntegerField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    temperatura = models.IntegerField(blank=True, null=True)
    consumo = models.CharField(max_length=30, blank=True, null=True)
    red = models.IntegerField(blank=True, null=True)
    bateria = models.IntegerField(blank=True, null=True)
    hora_actual = models.CharField(max_length=30, blank=True, null=True)
    #ubicacion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'vehiculos'
