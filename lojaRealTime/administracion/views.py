from concurrent.futures import ThreadPoolExecutor
import random
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import pyrebase
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import View 
import requests
# Importo Firebase Admin SDK 
import firebase_admin
# Hacemos uso de credenciales que nos permitirán usar Firebase Admin SDK 
from firebase_admin import credentials
# Importo el Servicio Cloud Firestore 
from firebase_admin import firestore
from datetime import datetime
from datetime import timedelta
from geopy.distance import geodesic
import googlemaps
import calendar

from administracion.models import Vehiculos

gmaps = googlemaps.Client(key='AIzaSyBmcEHbItWXSbgIH8BiQuD6Ns5bfyBoLtY')

def postAPI():
    url = "https://www.ktaxifacilsegurorapido.kradac.com/api/utpl/ultimaPosicion"

    payload='idCompania=7862254145&idCiudad=1&desde=1&hasta=1000&checksum=e43c681452041b00d393c1ac1a75da0e&token=4d4a8f40b9850decda9ab84dbed309c5c7e692591f97d76347fe019804b568d9'
    headers = {
    'version': '1.0.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic ZDRUMFN1VFBMOjNya1F3UDJ1NTNwdGxPZUJ5T3A1bQ=='
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    dic = response.json()
    return dic['lD']

def getUbicaciones(_request):
    if(len(postAPI()) >= 0):
        data = {'mensaje': "Correcto", "vehiculos":postAPI()}
    else:
        data = {'mensaje': "Error", "vehiculos":postAPI()}
    return JsonResponse(data)

#Funcion para calcular la distancia con latitud y longitud
def calcularDistancia(lng_A, lat_A, lng_B, lat_B):
    puntoA = (lat_A, lng_A)
    puntoB = (lat_B, lng_B)
    distancia = geodesic(puntoA, puntoB).km
    velocidad = distancia / 0.05

    return distancia, velocidad

def obtenerHora():
    #Obtencion de la hora actual
    horaFecha = datetime.now()
    horaFecha = horaFecha - timedelta(seconds=35)
    fechaActual = horaFecha.strftime("%D")
    horaActual = horaFecha.strftime("%H:%M")

    #Obtencion de la hora menos 3 min
    horaFechaAntigua = horaFecha - timedelta(minutes=3)
    horaAntigua = horaFechaAntigua.strftime("%H:%M")

    return (fechaActual + " " +  horaActual), (fechaActual + " " +  horaAntigua)
    
def getValoresMapa(_request):
    datosActuales = list()

    # Consulta que retorna todos los vehiculos en tiempo actual
    datosTiempoReal = Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[0])

    # Consulta que retorna todos los vehiculos en 3 min antes actual
    datosTiempoAtras = Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[1])

    for vehiculoActual in datosTiempoReal:
        for vehiculosAntiguo in datosTiempoAtras:
            if(vehiculoActual.id_vehiculo == vehiculosAntiguo.id_vehiculo):
                distanciaVelocidad = calcularDistancia(float(vehiculoActual.longitud), float(vehiculoActual.latitud), float(vehiculosAntiguo.longitud), float(vehiculosAntiguo.latitud))
                if (distanciaVelocidad[1] < 10 and (distanciaVelocidad[0] > 0.09 and distanciaVelocidad[0] < 0.4)):
                    dic = {"latitud": vehiculoActual.latitud, "longitud": vehiculoActual.longitud, "id_vehiculo" : vehiculoActual.id_vehiculo, "hora_actual": vehiculoActual.hora_actual, "distancia": round(distanciaVelocidad[0], 2), "velocidad" : round(distanciaVelocidad[1],2)}
                    datosActuales.append(dic)

    if(len(postAPI()) >= 0):
        data = {'mensaje': "Correcto", "totalVehiculos" : len(datosActuales), "vehiculos":datosActuales}
    else:
        data = {'mensaje': "Error", "totalVehiculos" : len(datosActuales),  "vehiculos":datosActuales}

    return JsonResponse(data)

def index(request):
    return render(request, "index.html", {"vehiculosActivos":len(postAPI())})

def proyecto(request):
    return render(request, "project.html")

def indicadores(request):
    
    avVelocidad = list()
    autosViasCongestion = list()
    viasCongestion = list()
    horasCongestion = list()
    viasMenorCongestion = list()

    # Consulta que retorna todos los vehiculos en tiempo actual
    datosTiempoReal = Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[0])

    # Consulta que retorna todos los vehiculos en 3 min antes actual
    datosTiempoAtras = Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[1])
    # Obtencion de las avenidas con mayor velocidad
    for vehiculoActual in datosTiempoReal:
        for vehiculosAntiguo in datosTiempoAtras:
            if(vehiculoActual.id_vehiculo == vehiculosAntiguo.id_vehiculo):
                distanciaVelocidad = calcularDistancia(float(vehiculoActual.longitud), float(vehiculoActual.latitud), float(vehiculosAntiguo.longitud), float(vehiculosAntiguo.latitud))
                if (distanciaVelocidad[1] > 30):
                    reverse_geocode_result = gmaps.reverse_geocode((vehiculoActual.latitud, vehiculoActual.longitud))
                    if("Av." in reverse_geocode_result[0]['formatted_address']):
                        try:
                            if(reverse_geocode_result[0]['address_components'][1]['types'] == ['route']):
                                avVelocidad.append(reverse_geocode_result[0]['address_components'][1]['long_name'])
                        except:
                            pass
                    else:
                        try:
                            if(reverse_geocode_result[0]['address_components'][1]['types'] == ['route']):
                                viasMenorCongestion.append(reverse_geocode_result[0]['address_components'][1]['long_name'])
                        except:
                            pass 
                elif(distanciaVelocidad[1] < 10):
                    autosViasCongestion.append([float(vehiculoActual.latitud), float(vehiculosAntiguo.longitud)])

    if len(autosViasCongestion) > 10:
        autosViasCongestion = random.choices(autosViasCongestion, k=7)
    
    for v in autosViasCongestion:
        reverse_geocode_result = gmaps.reverse_geocode((v[0], v[1]))
        try:
            if(reverse_geocode_result[0]['address_components'][1]['types'] == ['route']):
                viasCongestion.append(reverse_geocode_result[0]['address_components'][1]['long_name'])
        except:
            pass

    # Horarios de congestion de trafico 
    hora = datetime.now()
    fecha = hora.strftime("%D")
    rango = int(int(hora.strftime("%H:%M").split(":")[0])/ 2) - 2
    cHora = 6
    for i in range(1, rango + 1):
        datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = cHora).strftime("%H") and fecha + " " + hora.replace(hour = cHora + 1).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=10).count()
        horasCongestion.append([hora.replace(hour = cHora).strftime("%H")+":00 - " + hora.replace(hour = cHora+1).strftime("%H")+ ":59", datosHoras])
        cHora = cHora + 2
    
    horasCongestion = [x for x in horasCongestion if x[1] != 0]
    horasCongestion.sort(reverse=True)
    horasCongestion = horasCongestion[:5]
    # Vias centricas con menor congestion 
    viasMenorCongestion = set(viasMenorCongestion)
    avVelocidad = set(avVelocidad)
    viasCongestion = set(viasCongestion)
    if len(viasMenorCongestion) > 10:
        try:
            viasMenorCongestion = random.choices(viasMenorCongestion, k=10)
        except:
            pass

    return render(request, "indicadores.html", {"avVelocidad": avVelocidad, "viasCongestion": viasCongestion, "horasCongestion": horasCongestion , "viasMenorCongestion": viasMenorCongestion})

def login(request):
    return render(request, "login.html")

def dashboardIndicadores(request):
    return render(request, "dashboardIndicadores.html")

class EstadisticasPage(TemplateView):
    template_name = "estadisticas.html"

    def estadisticasPost(self):
        #Resumen del trfico (Mañana, tarde, noche)
        estadisticasDias = list()
        estadisticaManana = list()
        estadisticaTarde = list()
        estadisticaNoche = list()
        estadisticasSemana = list()
        horaFechaActual = datetime.now()
        fecha = horaFechaActual.strftime("%D")
        mes, dia, anio = (int(i) for i in fecha.split("/"))
        nroDia = calendar.weekday(anio, mes, dia)
        dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        
        if(dias[nroDia] == "Lunes"):
            horaFechaActual = horaFechaActual - timedelta(days = 7)
        elif(dias[nroDia] == "Martes"):
            horaFechaActual = horaFechaActual - timedelta(days = 8)
        elif(dias[nroDia] == "Miercoles"):
            horaFechaActual = horaFechaActual - timedelta(days = 9)
        elif(dias[nroDia] == "Jueves"):
            horaFechaActual = horaFechaActual - timedelta(days = 10)
        elif(dias[nroDia] == "Viernes"):
            horaFechaActual = horaFechaActual - timedelta(days = 11)
        elif(dias[nroDia] == "Sabado"):
            horaFechaActual = horaFechaActual - timedelta(days = 12)
        elif(dias[nroDia] == "Domingo"):
            horaFechaActual = horaFechaActual - timedelta(days = 6)
        
        fecha = horaFechaActual.strftime("%D")

        eManana = 0
        eTarde = 0
        eNoche = 0
        for x in range(1,8):
            for h in range(6,12):
                datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaFechaActual.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
                eManana = eManana + datosHoras

            for h in range(12,19):
                datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaFechaActual.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
                eTarde = eTarde + datosHoras

            for h in range(19,24):
                datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaFechaActual.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
                eNoche = eNoche + datosHoras
            
            horaFechaActual = horaFechaActual + timedelta(days = 1)
            fecha = horaFechaActual.strftime("%D")
            eManana = int(eManana / 6)
            eTarde = int(eTarde / 7)
            eNoche = int(eNoche / 5)
            estadisticasSemana.append(eManana + eTarde + eNoche)
            estadisticasDias.append([eManana, eTarde, eNoche])
            estadisticaManana.append(eManana)
            estadisticaTarde.append(eTarde)
            estadisticaNoche.append(eNoche)

        return estadisticasSemana, estadisticasDias, estadisticaManana, estadisticaTarde, estadisticaNoche

    def estadisticaHoy(self):
        #Resumen del trfico (Mañana, tarde, noche)
        hora = datetime.now()
        fecha = hora.strftime("%D")

        eManana = 0
        eTarde = 0
        eNoche = 0
        for h in range(6,12):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eManana = eManana + datosHoras

        for h in range(12,19):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eTarde = eTarde + datosHoras

        for h in range(19,24):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eNoche = eNoche + datosHoras
        
        eManana = int(eManana / 6)
        eTarde = int(eTarde / 7)
        eNoche = int(eNoche / 5)
        return [eManana, eTarde, eNoche]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estadisticas = self.estadisticasPost()
        context['estadisticasSemana'] = estadisticas[0]
        context['estadisticasDias'] = estadisticas[1]
        context['estadisticaManana'] = estadisticas[2]
        context['estadisticaTarde'] = estadisticas[3]
        context['estadisticaNoche'] = estadisticas[4]
        context['estadisticaDia'] = self.estadisticaHoy()

        return context
        
class DashboardPage(TemplateView):
    template_name = "dashboard.html"

    def calculosDashboard(self):
        listaVias = list()
        coordenadasVias = list()
        viasVelocidad = list(Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[0].split(" ")[0]).values_list('velocidad', 'latitud', 'longitud','id_vehiculo'))
        viasVelocidad.sort(reverse=True)
        viasVelocidad = viasVelocidad[:8]
        for c in viasVelocidad:
            reverse_geocode_result = gmaps.reverse_geocode((c[1], c[2]))
            try:
                if(reverse_geocode_result[0]['address_components'][1]['types'] == ['route']):
                    listaVias.append([reverse_geocode_result[0]['address_components'][1]['long_name'], c[0]])
                    coordenadasVias.append([c[1], c[2]])
            except:
                pass

        vehiculosHoy = len(Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[0].split(" ")[0]).values_list('id_usuario').distinct())
        vParados = len([x for x in postAPI() if x['velocidad'] == 0])

        #Resumen del trfico (Mañana, tarde, noche)
        hora = datetime.now()
        fecha = hora.strftime("%D")

        eManana = 0
        eTarde = 0
        eNoche = 0
        for h in range(6,12):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eManana = eManana + datosHoras

        for h in range(12,19):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eTarde = eTarde + datosHoras

        for h in range(19,24):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eNoche = eNoche + datosHoras
        
        eManana = int(eManana / 6)
        eTarde = int(eTarde / 7)
        eNoche = int(eNoche / 5)

        return len(postAPI()), vParados, vehiculosHoy, listaVias, eManana, eTarde, eNoche,coordenadasVias

    def obtenerSemana(self):

        estadisticaManana = list()
        estadisticaTarde = list()
        estadisticaNoche = list()
        horaFechaActual = datetime.now()
        fecha = horaFechaActual.strftime("%D")
        mes, dia, anio = (int(i) for i in fecha.split("/"))
        nroDia = calendar.weekday(anio, mes, dia)
        dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        
        if(dias[nroDia] == "Lunes"):
            horaFechaActual = horaFechaActual - timedelta(days = 7)
        elif(dias[nroDia] == "Martes"):
            horaFechaActual = horaFechaActual - timedelta(days = 8)
        elif(dias[nroDia] == "Miercoles"):
            horaFechaActual = horaFechaActual - timedelta(days = 9)
        elif(dias[nroDia] == "Jueves"):
            horaFechaActual = horaFechaActual - timedelta(days = 10)
        elif(dias[nroDia] == "Viernes"):
            horaFechaActual = horaFechaActual - timedelta(days = 11)
        elif(dias[nroDia] == "Sabado"):
            horaFechaActual = horaFechaActual - timedelta(days = 12)
        elif(dias[nroDia] == "Domingo"):
            horaFechaActual = horaFechaActual - timedelta(days = 6)
        
        fecha = horaFechaActual.strftime("%D")

        eManana = 0
        eTarde = 0
        eNoche = 0
        for x in range(1,8):
            for h in range(6,12):
                datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaFechaActual.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
                eManana = eManana + datosHoras

            for h in range(12,19):
                datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaFechaActual.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
                eTarde = eTarde + datosHoras

            for h in range(19,24):
                datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaFechaActual.replace(hour = h).strftime("%H"))).filter(velocidad__gte=3).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
                eNoche = eNoche + datosHoras
            
            horaFechaActual = horaFechaActual + timedelta(days = 1)
            fecha = horaFechaActual.strftime("%D")
            eManana = int(eManana / 6)
            eTarde = int(eTarde / 7)
            eNoche = int(eNoche / 5)
            estadisticaManana.append(eManana)
            estadisticaTarde.append(eTarde)
            estadisticaNoche.append(eNoche)

        return estadisticaManana, estadisticaTarde, estadisticaNoche
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datosDashboard = self.calculosDashboard()
        datosSemanales = self.obtenerSemana()
        context['vActivos'] = datosDashboard[0]
        context['vParados'] = datosDashboard[1]
        context['vehiculosHoy'] = datosDashboard[2]
        context['listaVias'] = datosDashboard[3]
        context['eManana'] = datosDashboard[4]
        context['eTarde'] = datosDashboard[5]
        context['eNoche'] = datosDashboard[6]
        context['coordenadasVias'] = datosDashboard[7]
        context['estadisticaManana'] = datosSemanales[0]
        context['estadisticaTarde'] = datosSemanales[1]
        context['estadisticaNoche'] = datosSemanales[2]
        return context

def rutasDash(_request):
    listaVias = list()
    viasVelocidad = list(Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[0].split(" ")[0]).values_list('velocidad', 'latitud', 'longitud','id_vehiculo'))
    viasVelocidad.sort(reverse=True)
    viasVelocidad = viasVelocidad[:8]
    for c in viasVelocidad:
        reverse_geocode_result = gmaps.reverse_geocode((c[1], c[2]))
        try:
            if(reverse_geocode_result[0]['address_components'][1]['types'] == ['route']):
                listaVias.append({"via": reverse_geocode_result[0]['address_components'][1]['long_name'] + ", Loja-Ecuador", "lat" : c[1], "long": c[2], 'velocidad':c[0]})
        except:
            pass

    if(len(listaVias) >= 0):
        data = {'mensaje': "Correcto", "vias": listaVias}
    else:
        data = {'mensaje': "Error", "vias": listaVias}
    return JsonResponse(data)

def ingreso(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"index.html",{"message":message})
        #return redirect("dashboard")
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    #return render(request,"dashboard.html",{"email":email.split("@")[0]}) 
    return redirect("dashboard")

# logout del sistema
def logout_view(request):
    message = "Has salido del sistema"
    try:
        del request.session['uid']
    except:
        pass
    #return render(request,"index.html",{"message":message, "vehiculosActivos":len(postAPI())})
    return redirect("index")

#Configuraciones del proyecto y la base de datos
config={
    "apiKey": "AIzaSyB_3NtWDjh-EXBpqx-zAKYk1DdA4Uyu7DA",
    "authDomain": "lojarealtime-b480a.firebaseapp.com",
    "databaseURL": "https://lojarealtime-b480a-default-rtdb.firebaseio.com",
    "projectId": "lojarealtime-b480a",
    "storageBucket": "lojarealtime-b480a.appspot.com",
    "messagingSenderId": "892103784621",
    "appId": "1:892103784621:web:1960109f370d8f0c51ee24",
    "measurementId": "G-3T15P7QS0Y",
}

# Llamo al archivo JSON que contiene mi clave privada
credenciales = credentials.Certificate("serviceAccountKey.json")
# Iniciamos los servicios de Firebase con las credenciales
firebase_admin.initialize_app(credenciales)
db = firestore.client()

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
