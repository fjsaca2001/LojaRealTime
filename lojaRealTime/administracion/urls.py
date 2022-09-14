"""
    Manejo de urls para la aplicación
    administracion
"""
from django.urls import path
# se importa las vistas de la aplicación
from . import views
from administracion.views import *

urlpatterns = [
   #path('', views.index, name="index"),
   path('', Index.as_view(), name="index"), 
   path('proyecto/', views.proyecto, name="proyecto"),
   path('dashboard/', views.dashboard, name="dashboard"),
   
   # Ingreso/Salida del sistema
    path('saliendo/logout/', views.logout_view, name="logout_view"),
    path('entrando/login/', views.ingreso, name="login"),

    # Url Para el Dashboard
    path('dashboard-realtime/', views.dashboardRealtime, name="dashboard-realtime"),
    path('dashboard-indicadores/', views.dashboardIndicadores, name="dashboard-indicadores"),
    path('dashboard-transito/', views.dashboardTransito, name="dashboard-transito"),
    path('dashboard-perfil/', views.dashboardPerfil, name="dashboard-perfil"),
]