from concurrent.futures import ThreadPoolExecutor
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
import math

from administracion.models import Vehiculos
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
    R = 6371.004
    pi = 3.141592654

    Mlng_A = lng_A
    Mlat_A = 90 - lat_A

    Mlng_B = lng_B
    Mlat_B = 90 - lat_B

    C = math.sin(Mlat_A*pi/180) * math.sin(Mlat_B*pi/180) * math.cos((Mlng_A - Mlng_B)*pi/180) +math.cos(Mlat_A*pi/180) * math.cos(Mlat_B*pi/180)

    if(C > 1):
        C = 1

    print("Cos: " + str(C))
    Distance = R * math.acos(C)

    return Distance

def getValoresMapa(_request):
    horaFecha = datetime.now()
    horaFecha = horaFecha - timedelta(seconds=35)
    fechaActual = horaFecha.strftime("%D")
    horaActual = horaFecha.strftime("%H:%M")
    datosActuales = list()
    datosAntiguos = list()

    # Consulta que retorna todos los vehiculos en tiempo actual
    datosTiempoReal = Vehiculos.objects.filter(hora_actual__startswith=fechaActual + " " +  horaActual)

    # Consulta que retorna todos los vehiculos en 3 min antes actual
    horaFechaAntigua = horaFecha - timedelta(minutes=3)
    horaAntigua = horaFechaAntigua.strftime("%H:%M")
    datosTiempoAtras = Vehiculos.objects.filter(hora_actual__startswith=fechaActual + " " +  horaAntigua)

    # Hora con 3 min atras
    horaFechaAntigua = horaFecha - timedelta(minutes=3)
    horaAntigua = horaFechaAntigua.strftime("%H:%M")

    for vehiculoActual in datosTiempoReal:
        for vehiculosAntiguo in datosTiempoAtras:
            if(vehiculoActual.id_vehiculo == vehiculosAntiguo.id_vehiculo):
                #print("lgA: " + vehiculoActual.longitud + " laA: " + vehiculoActual.latitud +" lgB: " +  vehiculosAntiguo.longitud + " laB: " +  vehiculosAntiguo.latitud)
                distancia = calcularDistancia(float(vehiculoActual.longitud), float(vehiculoActual.latitud), float(vehiculosAntiguo.longitud), float(vehiculosAntiguo.latitud))
                if (distancia < 0.5):
                    #print("Id_vehiculo: " + vehiculoActual.id_vehiculo + " La distancia es (Metros): " + str(round(distancia,1)))
                    dic = {"latitud": vehiculoActual.latitud, "longitud": vehiculoActual.longitud, "id_vehiculo" : vehiculoActual.id_vehiculo, "hora_actual": vehiculoActual.hora_actual}
                    datosActuales.append(dic)


    """for v in datosTiempoReal:
        dic = {"latitud": vehiculoActual.latitud, "longitud": vehiculoActual.longitud, "id_vehiculo" : vehiculoActual.id_vehiculo, "hora_actual": vehiculoActual.hora_actual}
        datosActuales.append(dic)
    """
    if(len(postAPI()) >= 0):
        data = {'mensaje': "Correcto", "vehiculos":datosActuales}
    else:
        data = {'mensaje': "Error", "vehiculos":datosActuales}
    return JsonResponse(data)

def index(request):
    return render(request, "index.html", {"vehiculosActivos":len(postAPI())})

def proyecto(request):
    return render(request, "project.html")

def indicadores(request):
    return render(request, "indicadores.html")

def login(request):
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")

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
    return render(request,"dashboard.html",{"email":email.split("@")[0]})
    #return redirect("dashboard")

# logout del sistema
def logout_view(request):
    message = "Has salido del sistema"
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"index.html",{"message":message, "vehiculosActivos":len(postAPI())})
    #return redirect("index")

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
