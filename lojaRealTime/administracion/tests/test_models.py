from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from administracion.views import *
from administracion.models import *

class TestModels(TestCase):

    def setUp(self):
        Vehiculos.objects.create(id_usuario="9307", velocidad=20)
        Vehiculos.objects.create(id_usuario="8932", velocidad=20)

    def test_exist_vehicle(self):

       vtest1 = Vehiculos.objects.get(id_usuario="9307")
       vtest2 = Vehiculos.objects.get(id_usuario="8932")

       print("Test de la base de datos")

       self.assertEqual(vtest1.velocidad, 20)
       self.assertEqual(vtest2.velocidad, 20)

