from django.test import SimpleTestCase
from django.urls import reverse, resolve
from administracion.views import *

class TestUrls(SimpleTestCase):

    def test_list_url_inicio(self):
        print("Prueba URL Inicio")
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)
    def test_list_url_proyecto(self):
        print("Prueba URL Proyecto")
        url = reverse('proyecto')
        print(resolve(url))
        self.assertEquals(resolve(url).func, proyecto)
    def test_list_url_estadistica(self):
        print("Prueba URL Movilidad")
        url = reverse('estadisticas')
        print(resolve(url))
        self.assertEquals(resolve(url).func, estadisticas)

    def test_list_url_login(self):
        print("Prueba URL Login")
        url = reverse('pageLogin')
        print(resolve(url))
        self.assertEquals(resolve(url).func, login)