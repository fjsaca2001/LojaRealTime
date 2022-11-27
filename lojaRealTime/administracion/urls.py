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
   # API cuando la fecha del grafico por dia cambie
    path('estadisticas/getValoresDashboardIndicadoresHistoricos/<fecha>', views.getValoresDashboardIndicadoresHistoricos, name="getValoresDashboardIndicadoresHistoricos"),
    # API cuando la fecha del grafico por dia cambie
    path('estadisticas/getValoresDashboardIndicadoresHistoricos2/<fecha>', views.getValoresDashboardIndicadoresHistoricos2, name="getValoresDashboardIndicadoresHistoricos2"),
    # API cuando la fecha del grafico reporte semanal cambie
    path('estadisticas/getValoresDashboardIndicadoresHistoricos3/<fecha>', views.getValoresDashboardIndicadoresHistoricos3, name="getValoresDashboardIndicadoresHistoricos3"),

   #path('estadisticas/', views.estadisticas, name="estadisticas"),
   #path('estadisticas/estadisticasPost/', views.estadisticasPost, name="estadisticasPost"),

   
   # Ingreso/Salida del sistema
    path('saliendo/logout/', views.logout_view, name="logout_view"),
    path('entrando/login/', views.ingreso, name="login"),

    # Url Para el Dashboard
    #path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/', DashboardPage.as_view(), name='dashboard'),
    path('dashboardIndicadoresHistoricos/', views.dashboardIndicadoresHistoricos, name="dashboardIndicadoresHistoricos"),

    # API cuando la fecha del grafico por dia cambie
    path('dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos/<fecha>', views.getValoresDashboardIndicadoresHistoricos, name="getValoresDashboardIndicadoresHistoricos"),

    # API cuando la fecha del grafico por dia cambie
    path('dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos2/<fecha>', views.getValoresDashboardIndicadoresHistoricos2, name="getValoresDashboardIndicadoresHistoricos2"),

    # API cuando la fecha del grafico reporte semanal cambie
    path('dashboardIndicadoresHistoricos/getValoresDashboardIndicadoresHistoricos3/<fecha>', views.getValoresDashboardIndicadoresHistoricos3, name="getValoresDashboardIndicadoresHistoricos3"),


    path('dashboard/getValoresMapaDash/', views.getValoresMapa, name="getValoresMapaDash"),
    path('dashboard/getRutasMapaDash/', views.rutasDash, name="getRutasMapaDash"),
    path('dashboard/controlTransito/getRutasMapaDashFecha/<fecha>', views.rutasDashFecha, name="getRutasMapaDashFecha"),
    path('dashboard/controlTransito/getUbicacionesCT/', views.getUbicaciones, name="getUbicacionesCT"),
    path('dashboard/controlTransito/', views.controlTransito, name="controlTransito"),
    path('dashboard/controlTransito/getVelocidades/<fechaMinima>/<fechaMaxima>', views.getVelocidades, name="getVelocidades"),
    path('dashboard/controlTransito/getVelocidadesPorId/<id1>/<id2>/<id3>', views.getVelocidadesPorId, name="getVelocidadesPorId"),
    path('dashboard/controlTransito/getVelocidadesPorIdAleatorio/', views.getVelocidadesPorIdAleatorio, name="getVelocidadesPorIdAleatorio"),
    path('dashboard/appEstadisticas/', views.appEstadisticas, name="appEstadisticas"),
    path('dashboard/appEstadisticas/getGPS', views.getGPS, name="getGPS"),
    path('dashboard/appEstadisticas/getGPSdia/<fecha>', views.getGPSdia, name="getGPSdia"),
    path('dashboard/getUbicacionesDash/', views.getUbicaciones, name="getUbicacionesDash"),
]