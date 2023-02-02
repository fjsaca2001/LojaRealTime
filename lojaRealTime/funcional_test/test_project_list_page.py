from selenium import webdriver
from administracion.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
import time


class TestProjectListPage(StaticLiveServerTestCase):
    """
    print("Pruebas de funcionalidad botones & carga inicial")

    def setUp(self):
        self.browser = webdriver.Chrome(
            '/home/fjsaca/Documentos/proyectoGit/LojaRealTime/lojaRealTime/funcional_test/chromedriver')

    def tearDown(self):
        self.browser.close()

    def test_no_projects_alert(self):
        self.browser.get(self.live_server_url)

        # Peticiones del usuario en primera instancia
        alert = self.browser.find_element(By.CLASS_NAME, 'head-index')
        self.assertEquals(
            alert.find_element(By.TAG_NAME, 'h1').text,
            'MOVILIDAD EN LA CIUDAD'
        )

    def test_alert_buttom_redirect_proyecto(self):

        self.browser.get(self.live_server_url)
        # Peticiones del usuario en primera instancia
        add_url = self.live_server_url + reverse('proyecto')

        self.browser.find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url + "proyecto/",
            add_url
        )

    def test_alert_buttom_redirect_inicio(self):

        self.browser.get(self.live_server_url)
        # Peticiones del usuario en primera instancia
        add_url = self.live_server_url + reverse('index')
 
        self.browser.find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url,
            add_url
        )

    def test_alert_buttom_redirect_movilidad(self):

        self.browser.get(self.live_server_url)
        # Peticiones del usuario en primera instancia
        add_url = self.live_server_url + reverse('estadisticas')
  
        self.browser.find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url + "estadisticas/",
            add_url
        )

    def test_alert_buttom_redirect_dashboard(self):

        self.browser.get(self.live_server_url)
        # Peticiones del usuario en primera instancia
        add_url = self.live_server_url + reverse('pageLogin')
        # time.sleep(20)
        self.browser.find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url + 'login/',
            add_url
        )
    """