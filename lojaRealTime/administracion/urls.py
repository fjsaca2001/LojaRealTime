"""
    Manejo de urls para la aplicación
    administracion
"""
from django.urls import path
# se importa las vistas de la aplicación
from . import views
from administracion.views import *

urlpatterns = [

    #Url para las vistas

   path('', views.index, name="index"), 
   path('proyecto/', views.proyecto, name="proyecto"),
   path('login/', views.login, name="pageLogin"),
   path('estadisticas/', views.estadisticas, name='estadisticas'),
   path('indicadores/', views.indicadores, name="indicadores"),

    #Dashboard

   path('dashboard/', DashboardPage.as_view(), name='dashboard'),
   path('dashboardIndicadoresHistoricos/', views.dashboardIndicadoresHistoricos, name="dashboardIndicadoresHistoricos"),
   path('dashboard/controlTransito/', views.controlTransito, name="controlTransito"),
   path('dashboard/appEstadisticas/', views.appEstadisticas, name="appEstadisticas"),

   #Urls como APIs

   path('getUbicaciones/', views.getUbicaciones, name="getUbicaciones"),
   path('getValoresMapa/', views.getValoresMapa, name="getValoresMapa"),
   
   # API cuando la fecha del grafico por dia cambie
    path('estadisticas/getValoresDashboardIndicadoresHistoricos/<fecha>', views.getValoresDashboardIndicadoresHistoricos, name="getValoresDashboardIndicadoresHistoricos"),
    # API cuando la fecha del grafico por dia cambie
    path('estadisticas/getValoresDashboardIndicadoresHistoricos2/<fecha>', views.getValoresDashboardIndicadoresHistoricos2, name="getValoresDashboardIndicadoresHistoricos2"),
    # API cuando la fecha del grafico reporte semanal cambie
    path('estadisticas/getValoresDashboardIndicadoresHistoricos3/<fecha>', views.getValoresDashboardIndicadoresHistoricos3, name="getValoresDashboardIndicadoresHistoricos3"),
   
   # Ingreso/Salida del sistema
    path('saliendo/logout/', views.logout_view, name="logout_view"),
    path('entrando/login/', views.ingreso, name="login"),

    # API cuando la fecha del grafico por dia cambie
    path('dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos/<fecha>', views.getValoresDashboardIndicadoresHistoricos, name="getValoresDashboardIndicadoresHistoricos"),

    # API cuando la fecha del grafico por dia cambie
    path('dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos2/<fecha>', views.getValoresDashboardIndicadoresHistoricos2, name="getValoresDashboardIndicadoresHistoricos2"),

    # API cuando la fecha del grafico reporte semanal cambie
    path('dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos3/<fecha>', views.getValoresDashboardIndicadoresHistoricos3, name="getValoresDashboardIndicadoresHistoricos3"),

    # API cuando la fecha del contador de taxis cambie
    path('dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricosTaxisActivos/<fecha>/', views.getValoresDashboardIndicadoresHistoricosTaxisActivos, name="getValoresDashboardIndicadoresHistoricosTaxisActivos"),
    
    path('dashboard/getValoresMapaDash/', views.getValoresMapa, name="getValoresMapaDash"),
    path('dashboard/getRutasMapaDash/', views.rutasDash, name="getRutasMapaDash"),
    path('dashboard/getUbicacionesDash/', views.getUbicaciones, name="getUbicacionesDash"), 

    path('dashboard/controlTransito/getRutasMapaDashFecha/<fecha>', views.rutasDashFecha, name="getRutasMapaDashFecha"),
    path('dashboard/controlTransito/getUbicacionesCT/', views.getUbicaciones, name="getUbicacionesCT"),
    path('dashboard/controlTransito/getVelocidades/<fechaMinima>/<fechaMaxima>', views.getVelocidades, name="getVelocidades"),
    path('dashboard/controlTransito/getVelocidadesPorId/<id1>/<id2>/<id3>', views.getVelocidadesPorId, name="getVelocidadesPorId"),
    path('dashboard/controlTransito/getVelocidadesPorIdAleatorio/', views.getVelocidadesPorIdAleatorio, name="getVelocidadesPorIdAleatorio"),


    path('dashboard/appEstadisticas/getGPS', views.getGPS, name="getGPS"),
    path('dashboard/appEstadisticas/getGPSdia/<fecha>', views.getGPSdia, name="getGPSdia"),
    path('dashboard/appEstadisticas/getConexion/<int:nroBtn>', views.getConexion, name="getConexion"),
    path('dashboard/appEstadisticas/getTemperatura/<idUsuario>/', views.getTemperatura, name="getTemperatura"),
    path('dashboard/appEstadisticas/getTemperaturaGeneral/<fechaTempGen>/', views.getTemperaturaGeneral, name="getTemperaturaGeneral"),
    path('dashboard/appEstadisticas/getTemperaturaAnalisis/<fechaTempGen>/', views.getTemperaturaAnalisis, name="getTemperaturaAnalisis"),
    path('dashboard/appEstadisticas/getConsumo/<idUsuario>/<horario>/<fecha>/', views.getConsumo, name="getConsumo"),
    path('dashboard/appEstadisticas/getConsumoGeneral/<fecha>/<int:btnValores>/', views.getConsumoGeneral, name="getConsumoGeneral"),
    path('dashboard/appEstadisticas/getBateria/<idUsuario>/<int:btnTiempo>/', views.getBateria, name="getBateria"),
    path('dashboard/appEstadisticas/getBateriaAhora/', views.getBateriaAhora, name="getBateriaAhora"),
]