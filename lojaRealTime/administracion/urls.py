"""
    Manejo de urls para la aplicación
    administracion
"""
from django.urls import path
# se importa las vistas de la aplicación
from . import views
from administracion.views import Zapatos

urlpatterns = [
   #path('', views.index, name="index"),
   path('postres/', Zapatos.as_view(), name="index"), 
]