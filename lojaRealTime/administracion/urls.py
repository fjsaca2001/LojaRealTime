"""
    Manejo de urls para la aplicación
    administracion
"""
from django.urls import path
# se importa las vistas de la aplicación
from . import views
from administracion.views import *

urlpatterns = [
   path('', views.index, name="index"), 
   path('proyecto/', views.proyecto, name="proyecto"),
   path('login/', views.login, name="pageLogin"),
   path('indicadores/', views.indicadores, name="indicadores"),
   
   # Ingreso/Salida del sistema
    path('saliendo/logout/', views.logout_view, name="logout_view"),
    path('entrando/login/', views.ingreso, name="login"),

    # Url Para el Dashboard
    path('dashboard/', views.dashboard, name="dashboard"),
]