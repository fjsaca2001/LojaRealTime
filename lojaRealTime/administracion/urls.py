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
   path('getUbicaciones/', views.getUbicaciones, name="getUbicaciones"),
   path('getValoresMapa/', views.getValoresMapa, name="getValoresMapa"),
   path('estadisticas/', EstadisticasPage.as_view(), name='estadisticas'),

   #path('estadisticas/', views.estadisticas, name="estadisticas"),
   #path('estadisticas/estadisticasPost/', views.estadisticasPost, name="estadisticasPost"),

   
   # Ingreso/Salida del sistema
    path('saliendo/logout/', views.logout_view, name="logout_view"),
    path('entrando/login/', views.ingreso, name="login"),

    # Url Para el Dashboard
    #path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/', DashboardPage.as_view(), name='dashboard'),
    path('dashboardIndicadoresHistoricos/', views.dashboardIndicadoresHistoricos, name="dashboardIndicadoresHistoricos"),
    path('dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos/<fecha>', views.getValoresDashboardIndicadoresHistoricos, name="getValoresDashboardIndicadoresHistoricos"),
    path('dashboard/getValoresMapaDash/', views.getValoresMapa, name="getValoresMapaDash"),
    path('dashboard/getRutasMapaDash/', views.rutasDash, name="getRutasMapaDash"),
    path('dashboard/getUbicacionesDash/', views.getUbicaciones, name="getUbicacionesDash"),
]