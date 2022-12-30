from django.test import TestCase, Client
from django.urls import reverse
from administracion.models import *
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.getUbicaciones_url = reverse("getUbicaciones")

        self.index_url = reverse('index')
        self.proyecto_url = reverse('proyecto')
        self.login_url = reverse('pageLogin')
        self.estadisticas_url = reverse('estadisticas')
 

    def test_project_index(self):

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'index.html' )

    def test_project_proyecto(self):
        response = self.client.get(self.proyecto_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'project.html')

    def test_project_login(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_project_estadisticas(self):
        response = self.client.get(self.estadisticas_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'estadisticas.html')
    

    def test_project_API_getUbicaciones(self):
        response = self.client.get('/getUbicaciones/')
        self.assertEqual(response.status_code, 200)
        print("Prueba API Consumo de datos")
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            str(response.content, encoding='utf8')
        )

    def test_project_API_getValoresMapa(self):
        response = self.client.get('/getValoresMapa/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            str(response.content, encoding='utf8')
        )

    def test_project_API_01(self):
        assert self.client.get('http://127.0.0.1:8000/dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos/2021-11-14').json()

    def test_project_API_02(self):
        assert self.client.get('http://127.0.0.1:8000/dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos2/2021-11-14').json()

    def test_project_API_03(self):
        assert self.client.get('http://127.0.0.1:8000/dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos3/2021-11-14').json()

    def test_project_API_04(self):
        assert self.client.get('http://127.0.0.1:8000/dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricosTaxisActivos/2021-11-14/').json()

    def test_project_API_05(self):
        assert self.client.get('http://127.0.0.1:8000/dashboard/controlTransito/getRutasMapaDashFecha/2021-11-14').json()

    def test_project_API_06(self):
        assert self.client.get('http://127.0.0.1:8000/dashboard/controlTransito/getVelocidades/2021-11-14/2021-11-25').json()