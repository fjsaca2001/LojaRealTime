import random
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render, redirect
import pyrebase
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
import sqlite3
from administracion.models import Vehiculos

# Clave Api google Maps
gmaps = googlemaps.Client(key='AIzaSyBmcEHbItWXSbgIH8BiQuD6Ns5bfyBoLtY')

#Funcion para calcular la distancia y velocidad con latitud y longitud
def calcularDistancia(lng_A, lat_A, lng_B, lat_B):
    puntoA = (lat_A, lng_A)
    puntoB = (lat_B, lng_B)
    distancia = geodesic(puntoA, puntoB).km
    velocidad = distancia / 0.05

    return distancia, velocidad

# Funcion para obtener la hora actual
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

# Validacion del usuario y contraseña
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

# Funcion utilizada para obtener los datos desde la base de datos
# Recibe como parametro una consulta sql
def consultaBASE(csql):

    con = sqlite3.connect("/home/fjsaca/Documentos/proyectoGit/LojaRealTime/flask/tempVehiculos.db")
    cur = con.cursor()
    cur.execute(csql)
    valores = cur.fetchall()

    return valores

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

"""
    * JsonResponse como API's
"""

# Obtencion de los datos de kradac
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

# Api que obtiene datos de los taxis
def getUbicaciones(_request):
    if(len(postAPI()) >= 0):
        data = {'mensaje': "Correcto", "vehiculos":postAPI()}
    else:
        data = {'mensaje': "Error", "vehiculos":postAPI()}
    return JsonResponse(data)

# Api que obtiene los puntos de calor en la pagina principal
def getValoresMapa(_request):
    datosActuales = list()

    # Consulta que retorna todos los vehiculos en tiempo actual
    datosTiempoReal = Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[0])

    # Consulta que retorna todos los vehiculos en 3 min antes actual
    datosTiempoAtras = Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[1])

    # Recorrido de los datos antiguos y nuevos 
    for vehiculoActual in datosTiempoReal:
        for vehiculosAntiguo in datosTiempoAtras:
            #Comparacion que valida que sea el mismo vehiculo
            if(vehiculoActual.id_vehiculo == vehiculosAntiguo.id_vehiculo):
                distanciaVelocidad = calcularDistancia(float(vehiculoActual.longitud), float(vehiculoActual.latitud), float(vehiculosAntiguo.longitud), float(vehiculosAntiguo.latitud))
                # Comparacion de la velocidad y distancia recorrida
                if (distanciaVelocidad[1] < 7 and (distanciaVelocidad[0] > 0.1 and distanciaVelocidad[0] < 0.3)):
                    dic = {"latitud": vehiculoActual.latitud, "longitud": vehiculoActual.longitud, "id_vehiculo" : vehiculoActual.id_vehiculo, "hora_actual": vehiculoActual.hora_actual, "distancia": round(distanciaVelocidad[0], 2), "velocidad" : round(distanciaVelocidad[1],2)}
                    datosActuales.append(dic)

    if(len(postAPI()) >= 0):
        data = {'mensaje': "Correcto", "totalVehiculos" : len(datosActuales), "vehiculos":datosActuales}
    else:
        data = {'mensaje': "Error", "totalVehiculos" : len(datosActuales),  "vehiculos":datosActuales}

    return JsonResponse(data)

# Api que retorna el nombre de la via con lat y long 
# Para marcar las rutas en el dashboard
def rutasDash(_request):
    listaVias = list()
    viasVelocidad = list(Vehiculos.objects.filter(hora_actual__startswith=obtenerHora()[0].split(" ")[0]).values_list('velocidad', 'latitud', 'longitud','id_vehiculo'))
    viasVelocidad.sort(reverse=True)
    viasVelocidad = viasVelocidad[:8]
    for c in viasVelocidad:
        reverse_geocode_result = gmaps.reverse_geocode((c[1], c[2]))
        try:
            if(reverse_geocode_result[0]['address_components'][1]['types'] == ['route']):
                if(len(reverse_geocode_result[0]['address_components'][1]['long_name']) > 3):
                    listaVias.append({"via": reverse_geocode_result[0]['address_components'][1]['long_name'] + ", Loja-Ecuador", "lat" : c[1], "long": c[2], 'velocidad':c[0]})
        except:
            pass

    if(len(listaVias) > 0):
        data = {'mensaje': "Correcto", "vias": listaVias}
    else:
        data = {'mensaje': "Error", "vias": listaVias}
    return JsonResponse(data)

# Api para el control de trafico por fecha 
# usada en el control de transito para 
# colocar el nombre de las vias
def rutasDashFecha(_request, fecha):
    listaVias = list()
    fechaSeparada = fecha.split("-") #anio-mes-dia 2021-11-14
    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia
    fecha = horaHistorica.strftime("%D")
    viasVelocidad = list(Vehiculos.objects.filter(hora_actual__startswith=fecha).values_list('velocidad', 'latitud', 'longitud','id_vehiculo'))
    viasVelocidad.sort(reverse=True)
    viasVelocidad = viasVelocidad[:12]
    print(viasVelocidad)
    for c in viasVelocidad:
        reverse_geocode_result = gmaps.reverse_geocode((c[1], c[2]))
        try:
            if(reverse_geocode_result[0]['address_components'][1]['types'] == ['route']):
                if(len(reverse_geocode_result[0]['address_components'][1]['long_name']) > 3):
                    listaVias.append({"via": reverse_geocode_result[0]['address_components'][1]['long_name'] + ", Loja-Ecuador", "lat" : c[1], "long": c[2], 'velocidad':c[0]})
        except:
            pass

    if(len(listaVias) >= 0):
        data = {'mensaje': "Correcto", "vias": listaVias}
    else:
        data = {'mensaje': "Error", "vias": listaVias}
    return JsonResponse(data)

# API cuando la fecha del grafico por dia cambie 
# usado en el control de transito y movilidad 
# para la grafica que presenta la semana, por dia y horario
def getValoresDashboardIndicadoresHistoricos(_request, fecha):
    estadisticaManana = list()
    estadisticaTarde = list()
    estadisticaNoche = list()
    fechaSeparada = fecha.split("-") #anio-mes-dia 2021-11-14
    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia
    nroDia = calendar.weekday(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2]))
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

    if(dias[nroDia] == "Lunes"):
            horaHistorica = horaHistorica - timedelta(days = 7)
    elif(dias[nroDia] == "Martes"):
            horaHistorica = horaHistorica - timedelta(days = 8)
    elif(dias[nroDia] == "Miercoles"):
            horaHistorica = horaHistorica - timedelta(days = 9)
    elif(dias[nroDia] == "Jueves"):
            horaHistorica = horaHistorica - timedelta(days = 10)
    elif(dias[nroDia] == "Viernes"):
            horaHistorica = horaHistorica - timedelta(days = 11)
    elif(dias[nroDia] == "Sabado"):
            horaHistorica = horaHistorica - timedelta(days = 12)
    elif(dias[nroDia] == "Domingo"):
            horaHistorica = horaHistorica - timedelta(days = 6)
        
    fecha = horaHistorica.strftime("%D")

    eManana = 0
    eTarde = 0
    eNoche = 0
    for x in range(1,8):
        for h in range(6,12):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaHistorica.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eManana = eManana + datosHoras

        for h in range(12,19):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaHistorica.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eTarde = eTarde + datosHoras

        for h in range(19,24):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaHistorica.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eNoche = eNoche + datosHoras
        
        horaHistorica = horaHistorica + timedelta(days = 1)
        fecha = horaHistorica.strftime("%D")
        eManana = int(eManana / 6)
        eTarde = int(eTarde / 7)
        eNoche = int(eNoche / 5)
        estadisticaManana.append(eManana)
        estadisticaTarde.append(eTarde)
        estadisticaNoche.append(eNoche)

    
        
    print(fecha)
    if(len(estadisticaManana) > 0):
        data = {'mensaje': "Correcto","estadisticaManana": estadisticaManana, "estadisticaTarde": estadisticaTarde, "estadisticaNoche": estadisticaNoche , "fecha": fecha}
    else:
        data = {'mensaje': "Error", "fecha": fecha}

    return JsonResponse(data)

# API cuando la fecha del grafico por dia cambie
# usado en el control de transito y movilidad 
# para la grafica que presenta la dia y horario
def getValoresDashboardIndicadoresHistoricos2(_request, fecha):
    fechaSeparada = fecha.split("-") #anio-mes-dia 2021-11-14.

    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia

    fecha = horaHistorica.strftime("%D")

    print(fecha)

    eManana = 0
    eTarde = 0
    eNoche = 0

    for h in range(6,12):
        datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaHistorica.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
        eManana = eManana + datosHoras

    for h in range(12,19):
        datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaHistorica.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
        eTarde = eTarde + datosHoras

    for h in range(19,24):
        datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaHistorica.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
        eNoche = eNoche + datosHoras
    
    eManana = int(eManana / 6)
    eTarde = int(eTarde / 7)
    eNoche = int(eNoche / 5)

    data = {'mensaje': "Correcto","eManana": eManana, "eTarde": eTarde, "eNoche": eNoche , "fecha": fecha}

    return JsonResponse(data)

# API cuando la fecha del grafico reporte semanal cambie
# usado en el control de transito y movilidad 
# para la grafica que presenta la semana por dia
def getValoresDashboardIndicadoresHistoricos3(_request, fecha):

    estadisticasSemana = list()

    fechaSeparada = fecha.split("-") #anio-mes-dia 2021-11-14
    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia
    nroDia = calendar.weekday(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2]))
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    print(horaHistorica)
    if(dias[nroDia] == "Lunes"):
            horaHistorica = horaHistorica - timedelta(days = 7)
    elif(dias[nroDia] == "Martes"):
            horaHistorica = horaHistorica - timedelta(days = 8)
    elif(dias[nroDia] == "Miercoles"):
            horaHistorica = horaHistorica - timedelta(days = 9)
    elif(dias[nroDia] == "Jueves"):
            horaHistorica = horaHistorica - timedelta(days = 10)
    elif(dias[nroDia] == "Viernes"):
            horaHistorica = horaHistorica - timedelta(days = 11)
    elif(dias[nroDia] == "Sabado"):
            horaHistorica = horaHistorica - timedelta(days = 12)
    elif(dias[nroDia] == "Domingo"):
            horaHistorica = horaHistorica - timedelta(days = 6)
        
    fecha = horaHistorica.strftime("%D")
    
    print(fecha)
    eManana = 0
    eTarde = 0
    eNoche = 0

    for x in range(1,8):
        for h in range(6,12):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaHistorica.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eManana = eManana + datosHoras

        for h in range(12,19):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaHistorica.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eTarde = eTarde + datosHoras

        for h in range(19,24):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaHistorica.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eNoche = eNoche + datosHoras
            
        horaHistorica = horaHistorica + timedelta(days = 1)
        fecha = horaHistorica.strftime("%D")
        eManana = int(eManana / 6)
        eTarde = int(eTarde / 7)
        eNoche = int(eNoche / 5)
        
        estadisticasSemana.append(eManana + eTarde + eNoche)

    data = {'mensaje': "Correcto","estadisticasSemana": estadisticasSemana , "fecha": fecha}

    return JsonResponse(data)

# API cuando la fecha del grafico taxis activos cambie
# usado en estadisticas del App para la grafica que presenta
# los taxis activos por dia
def getValoresDashboardIndicadoresHistoricosTaxisActivos(_request, fecha):

    hManana = ("06","07","08","09","10","11", "12")
    hTarde = ("13","14","15","14","17", "18")
    hNoche = ("19","20","21","22","23", "00")

    fechaSeparada = fecha.split("-") #anio-mes-dia 2021-11-14
    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia
    fecha = horaHistorica.strftime("%D")

    consulta = "SELECT DISTINCT id_usuario FROM vehiculos WHERE hora_actual LIKE '" + fecha + " " + hManana[0] + "%' OR hora_actual LIKE '" + fecha + " " + hManana[1] + "%' OR hora_actual LIKE '" + fecha + " " + hManana[2] + "%' OR hora_actual LIKE '" + fecha + " " + hManana[3] + "%' OR hora_actual LIKE '" + fecha + " " + hManana[4] + "%' OR hora_actual LIKE '" + fecha + " " + hManana[5] + "%' OR hora_actual LIKE '" + fecha + " " + hManana[6] + "%'"
    sumaManana = len(consultaBASE(consulta))

    consulta = "SELECT DISTINCT id_usuario FROM vehiculos WHERE hora_actual LIKE '" + fecha + " " + hTarde[0] + "%' OR hora_actual LIKE '" + fecha + " " + hTarde[1] + "%' OR hora_actual LIKE '" + fecha + " " + hTarde[2] + "%' OR hora_actual LIKE '" + fecha + " " + hTarde[3] + "%' OR hora_actual LIKE '" + fecha + " " + hTarde[4] + "%' OR hora_actual LIKE '" + fecha + " " + hTarde[5] + "%'"
    sumaTarde = len(consultaBASE(consulta))

    consulta = "SELECT DISTINCT id_usuario FROM vehiculos WHERE hora_actual LIKE '" + fecha + " " + hNoche[0] + "%' OR hora_actual LIKE '" + fecha + " " + hNoche[1] + "%' OR hora_actual LIKE '" + fecha + " " + hNoche[2] + "%' OR hora_actual LIKE '" + fecha + " " + hNoche[3] + "%' OR hora_actual LIKE '" + fecha + " " + hNoche[4] + "%' OR hora_actual LIKE '" + fecha + " " + hNoche[5] + "%'"
    sumaNoche = len(consultaBASE(consulta))

    data = {'mensaje': "Correcto", "sumaManana": sumaManana, "sumaTarde": sumaTarde, "sumaNoche": sumaNoche}

    return JsonResponse(data)

# API cuando el usuario ingrese ids de usuarios
# usado en indicadores de movilidad para la grafica que presenta
# las velocidades en promedio
def getVelocidadesPorId(_request, id1, id2, id3):

    listaId1 = list()
    listaId2 = list()
    listaId3 = list()
    listaDias = list()
    listaUsuarios = list()
    consulta = "SELECT DISTINCT id_usuario FROM vehiculos WHERE id_vehiculo = "+id1
    listaUsuarios.append([consultaBASE(consulta)[0][0] if len(consultaBASE(consulta)) > 0 else 0, id1])
    consulta = "SELECT DISTINCT id_usuario FROM vehiculos WHERE id_vehiculo = "+id2
    listaUsuarios.append([consultaBASE(consulta)[0][0] if len(consultaBASE(consulta)) > 0 else 0, id2])
    consulta = "SELECT DISTINCT id_usuario FROM vehiculos WHERE id_vehiculo = "+id3
    listaUsuarios.append([consultaBASE(consulta)[0][0] if len(consultaBASE(consulta)) > 0 else 0, id3])
    horaFecha = datetime.now()
    horaFecha = horaFecha - timedelta(days=5)
    fecha = horaFecha.strftime("%D")
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

    for d in range(1,6):
        fecha = fecha.split("/")
        nroDia = calendar.weekday(int(fecha[2]), int(fecha[0]), int(fecha[1]))
        listaDias.append(dias[nroDia])
        horaFecha = horaFecha + timedelta(days=1)
        fecha = horaFecha.strftime("%D")

        consulta = "SELECT ROUND(AVG(velocidad), 2) FROM vehiculos WHERE id_vehiculo = '" + id1 + "' AND hora_actual LIKE '" + fecha + "%'"
        valores = consultaBASE(consulta)
        listaId1.append(valores[0][0])
        
        consulta = "SELECT ROUND(AVG(velocidad), 2) FROM vehiculos WHERE id_vehiculo = '" + id2 + "' AND hora_actual LIKE '" + fecha + "%'"
        valores = consultaBASE(consulta)
        listaId2.append(valores[0][0])

        consulta = "SELECT ROUND(AVG(velocidad), 2) FROM vehiculos WHERE id_vehiculo = '" + id3 + "' AND hora_actual LIKE '" + fecha + "%'"
        valores = consultaBASE(consulta)
        listaId3.append(valores[0][0])

    data = {'mensaje': "Correcto", "listaUsuarios": listaUsuarios, "listaDias": listaDias, "listaId1": listaId1, "listaId2": listaId2, "listaId3": listaId3}

    return JsonResponse(data)

# API cuando el usuario desee aleatoriamente ids de usuarios
# usado en indicadores de movilidad para la grafica que presenta
# las velocidades en promedio
def getVelocidadesPorIdAleatorio(_request):
    valores = postAPI()
    ids = (valores[random.randint(0, len(postAPI()))]['id_vehiculo'], valores[random.randint(0, len(postAPI()))]['id_vehiculo'],valores[random.randint(0, len(postAPI()))]['id_vehiculo'])
    data = {'mensaje': "Correcto", "ids": ids}

    return JsonResponse(data)

# API cuando el usuario desee ver los dispositivos con el gps
# encendido o apagado, usado en estadisticas del app 
# para la grafica que presenta los dis. gps on/off
def getGPS(_request):

    fechaHoy = obtenerHora()[0]
    fechaHoy = fechaHoy.split(" ")[0]
 
    consultaGPS0 = "select DISTINCT id_usuario, id_vehiculo from vehiculos WHERE gps = 0 and hora_actual LIKE '" + fechaHoy +"%'"
    
    consultaGPS1 = "select DISTINCT id_usuario, id_vehiculo from vehiculos WHERE gps = 1 and hora_actual LIKE '" + fechaHoy + "%'"

    gps0 = consultaBASE(consultaGPS0)
    gps1 = consultaBASE(consultaGPS1)

    data = {'mensaje': "Correcto", "totalGPS0": len(gps0), "totalGPS1": len(gps1), "dataGPS0": gps0}

    return JsonResponse(data)

# API cuando el usuario desee ver los dispositivos con el gps
# encendido o apagado, usado en estadisticas del app 
# para la grafica que presenta los dis. gps on/off por dia
def getGPSdia(_request, fecha):

    fechaSeparada = fecha.split("-") #anio-mes-dia 2021-11-14
    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia
    fecha = horaHistorica.strftime("%D")

    consultaGPS0 = "select DISTINCT id_usuario, id_vehiculo from vehiculos WHERE gps = 0 and hora_actual LIKE '" + fecha +"%'"
    
    consultaGPS1 = "select DISTINCT id_usuario, id_vehiculo from vehiculos WHERE gps = 1 and hora_actual LIKE '" + fecha + "%'"

    gps0 = consultaBASE(consultaGPS0)
    gps1 = consultaBASE(consultaGPS1)

    data = {'mensaje': "Correcto", "totalGPS0": len(gps0), "totalGPS1": len(gps1), "dataGPS0": gps0}

    return JsonResponse(data)

# API cuando el usuario desee ver los tipos de conexion
# usado en estadisticas del app para la grafica que presenta
# los tipos de conexion, en los ultimos dias
def getConexion(_request, nroBtn):
    # nroBtn = 0 -> 7 Dias; nroBtn = 15 Dias -> 3g; nroBtn = 2 -> 1 mes

    listaDias = list() # Divicion por dias
    lista3G = list() # Divicion 3g
    lista4G = list() # Divicion 4g
    listaWifi = list() # Divicion wifi

    horaFecha = datetime.now()

    if(nroBtn == 0):
        horaFecha = horaFecha - timedelta(days=7)
        dias = 7
    elif(nroBtn == 1):
        horaFecha = horaFecha - timedelta(days=15)
        dias = 15
    elif(nroBtn == 2):
        horaFecha = horaFecha - timedelta(days=30)
        dias = 30

    # 0 -> Wifi; 1 -> 3g; 2 -> 4g
    
    diasS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    for d in range(0, dias):
        fecha = horaFecha.strftime("%D")
        print(fecha)
        consultaConexionWifi = "SELECT DISTINCT id_usuario, conexion FROM vehiculos WHERE hora_actual LIKE '" + fecha +"%' AND conexion = 0 ORDER BY id_usuario"

        consultaConexion3g = "SELECT DISTINCT id_usuario, conexion FROM vehiculos WHERE hora_actual LIKE '" + fecha +"%' AND conexion = 1 ORDER BY id_usuario"

        consultaConexion4g = "SELECT DISTINCT id_usuario, conexion FROM vehiculos WHERE hora_actual LIKE '" + fecha +"%' AND conexion = 2 ORDER BY id_usuario"

        dbwifi = consultaBASE(consultaConexionWifi)
        db3g = consultaBASE(consultaConexion3g)
        db4g = consultaBASE(consultaConexion4g)
        nroDia = calendar.weekday(int(fecha.split("/")[2]), int(fecha.split("/")[0]), int(fecha.split("/")[1]))
        listaWifi.append(len(dbwifi))
        lista3G.append(len(db3g))
        lista4G.append(len(db4g))
        listaDias.append(diasS[nroDia] + ", " +fecha.split("/")[1])

        horaFecha = horaFecha + timedelta(days=1)

    data = {'mensaje': "Correcto", "listaWifi": listaWifi, "lista3G": lista3G, "lista4G": lista4G , "listaDias": listaDias,"fecha": fecha}

    return JsonResponse(data)

# API cuando el usuario desee ver el promedio de temperatura
# usado en estadisticas del app para la grafica que presenta
# la temperatura de los dispositivos de los ultimos 7 dias,
# Separado por horarios
def getTemperatura(_request, idUsuario):
 
    hManana = ("06","07","08","09","10","11")
    hTarde = ("12","13","14","15","14","17")
    hNoche = ("18","19","20","21","22","23")

    listaManana = list() # Divicion por dias
    listaTarde = list() # Divicion 3g
    listaNoche = list() # Divicion 4g
    listaDias = list()
    horaFecha = datetime.now()
    horaFecha = horaFecha - timedelta(days=7)

    diasS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    #SELECT id_usuario, ROUND(AVG(temperatura),1) FROM vehiculos WHERE id_usuario = '2731' AND hora_actual LIKE '11/22/22 07%'
    for d in range (0,7):
        sumaManana = 0
        sumaTarde = 0
        sumaNoche = 0
        fecha = horaFecha.strftime("%D")
        nroDia = calendar.weekday(int(fecha.split("/")[2]), int(fecha.split("/")[0]), int(fecha.split("/")[1]))

        for h in range(0,5):
            consultaHmanana = "SELECT ROUND(AVG(temperatura),1) FROM vehiculos WHERE id_usuario = '" + idUsuario + "' AND hora_actual LIKE '" + fecha + " " + hManana[h] + "%'"
            dbManana = consultaBASE(consultaHmanana)
            sumaManana = sumaManana + int(dbManana[0][0] or 0)
            
            consultaHmanana = "SELECT ROUND(AVG(temperatura),1) FROM vehiculos WHERE id_usuario = '" + idUsuario + "' AND hora_actual LIKE '" + fecha + " " + hTarde[h] + "%'"
            dbManana = consultaBASE(consultaHmanana)
            sumaTarde = sumaTarde + int(dbManana[0][0] or 0)

            consultaHmanana = "SELECT ROUND(AVG(temperatura),1) FROM vehiculos WHERE id_usuario = '" + idUsuario + "' AND hora_actual LIKE '" + fecha + " " + hNoche[h] + "%'"
            dbManana = consultaBASE(consultaHmanana)
            sumaNoche = sumaNoche + int(dbManana[0][0] or 0)
        
        horaFecha = horaFecha + timedelta(days=1)

        listaManana.append(round(sumaManana/6, 1))
        listaTarde.append(round(sumaTarde/6, 1))
        listaNoche.append(round(sumaNoche/6, 1))

        for x in range(0, len(listaManana)):
            if(listaManana[x] == 0):
                listaManana[x] = "null"
            
            if(listaTarde[x] == 0):
                listaTarde[x] = "null"

            if(listaNoche[x] == 0):
                listaNoche[x] = "null"

        
        listaDias.append(diasS[nroDia] + ", " +fecha.split("/")[1])

    data = {'mensaje': "Correcto", "listaManana": listaManana, "listaTarde": listaTarde, "listaNoche": listaNoche, "listaDias": listaDias}

    return JsonResponse(data)

# API cuando el usuario desee ver el promedio de temperatura
# usado en estadisticas del app para la grafica que presenta
# la temperatura del dia ingresado separado por horarios
def getTemperaturaGeneral(_request, fechaTempGen):
    
    fechaSeparada = fechaTempGen.split("-") #anio-mes-dia 2021-11-14
    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia
    fecha = horaHistorica.strftime("%D")

    hManana = ("06","07","08","09","10","11")
    hTarde = ("12","13","14","15","14","17")
    hNoche = ("18","19","20","21","22","23")

    rManana = 0
    rTarde = 0 
    rNoche = 0


    for h in range(0,5):
        consultaHmanana = "SELECT ROUND(AVG(temperatura),1) FROM vehiculos WHERE hora_actual LIKE '" + fecha + " " + hManana[h] + "%'"
        dbManana = consultaBASE(consultaHmanana)
        rManana = rManana + int(dbManana[0][0] or 0)
            
        consultaHmanana = "SELECT ROUND(AVG(temperatura),1) FROM vehiculos WHERE hora_actual LIKE '" + fecha + " " + hTarde[h] + "%'"
        dbManana = consultaBASE(consultaHmanana)
        rTarde = rTarde + int(dbManana[0][0] or 0)

        consultaHmanana = "SELECT ROUND(AVG(temperatura),1) FROM vehiculos WHERE hora_actual LIKE '" + fecha + " " + hNoche[h] + "%'"
        dbManana = consultaBASE(consultaHmanana)
        rNoche = rNoche + int(dbManana[0][0] or 0)

    data = {'mensaje': "Correcto", "rManana": round(rManana/6,1), "rTarde": round(rTarde/6,1), "rNoche": round(rNoche/6,1)}

    return JsonResponse(data)

# API cuando el usuario desee ver el promedio de temperatura
# usado en estadisticas del app para la grafica que presenta
# la temperatura del dia ingresado separado por rangos
# mayor - menor e igual a 30°c
def getTemperaturaAnalisis(_request, fechaTempGen):
    
    fechaSeparada = fechaTempGen.split("-") #anio-mes-dia 2021-11-14
    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia
    fecha = horaHistorica.strftime("%D")
    #SELECT temperatura FROM vehiculos WHERE hora_actual LIKE '11/22/22%' AND temperatura = 30 GROUP BY id_usuario
    consulta = "SELECT temperatura FROM vehiculos WHERE hora_actual LIKE '" + fecha + "%' AND temperatura > 30 GROUP BY id_usuario"
    resultConsulta = consultaBASE(consulta)
    mas30 = len(resultConsulta)
            
    consulta = "SELECT temperatura FROM vehiculos WHERE hora_actual LIKE '" + fecha + "%' AND (temperatura < 30 AND temperatura > 0) GROUP BY id_usuario"
    resultConsulta = consultaBASE(consulta)
    menos30 = len(resultConsulta)

    consulta = "SELECT temperatura FROM vehiculos WHERE hora_actual LIKE '" + fecha + "%' AND temperatura = 30 GROUP BY id_usuario"
    resultConsulta = consultaBASE(consulta)
    igual30 = len(resultConsulta)

    consulta = "SELECT temperatura FROM vehiculos WHERE hora_actual LIKE '" + fecha + "%' AND temperatura = 0 GROUP BY id_usuario"
    resultConsulta = consultaBASE(consulta)
    igual0 = len(resultConsulta)

    data = {'mensaje': "Correcto", "mas30": mas30, "menos30": menos30, "igual30": igual30, "igual0": igual0}

    return JsonResponse(data)

# API cuando el usuario desee ver el promedio de consumo
# usado en estadisticas del app para la grafica que presenta
# el consumo del dia ingresado separado por rangos horarios
# tambien ingresados
def getConsumo(_request, idUsuario, horario, fecha):

    if(horario == "manana"):
        horas = ("06","07","08","09","10","11")
    elif(horario == "tarde"):
        horas = ("12","13","14","15","14","17")
    else:
        horas = ("18","19","20","21","22","23")

    listaConsumo = list() # Divicion por dias

    fechaSeparada = fecha.split("-") #anio-mes-dia 2021-11-14
    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia
    fecha = horaHistorica.strftime("%D")

    #SELECT ROUND(AVG(consumo),1) FROM vehiculos WHERE id_usuario = '2731' AND hora_actual LIKE '11/22/22 07%'
    for h in horas:
        consulta = "SELECT ROUND(AVG(consumo),1) FROM vehiculos WHERE id_usuario = '" + idUsuario + "' AND hora_actual LIKE '" + fecha + " " + h + "%'"
        dbManana = consultaBASE(consulta)
        listaConsumo.append(int(dbManana[0][0] or 0))

    for x in range(0, len(listaConsumo)):
        if(listaConsumo[x] == 0):
            listaConsumo[x] = "null"

    data = {'mensaje': "Correcto", "listaConsumo": listaConsumo, "horas": horas}

    return JsonResponse(data)

# API cuando el usuario desee ver el promedio de consumo
# usado en estadisticas del app para la grafica que presenta
# el consumo del dia ingresado separado por rangos 
# tambien ingresados, mayores, menores y todo
def getConsumoGeneral(_request, fecha, btnValores):

    fechaSeparada = fecha.split("-") #anio-mes-dia 2021-11-14
    horaHistorica = datetime(int(fechaSeparada[0]), int(fechaSeparada[1]), int(fechaSeparada[2])) #Anio - mes - dia
    fecha = horaHistorica.strftime("%D")

    #SELECT id_usuario, ROUND(AVG(consumo),1) AS promConsumo FROM vehiculos WHERE hora_actual LIKE '11/22/22%' GROUP BY id_usuario ORDER BY promConsumo

    consulta = "SELECT id_usuario, ROUND(AVG(consumo),1) AS promConsumo FROM vehiculos WHERE hora_actual LIKE '" + fecha +"%' GROUP BY id_usuario ORDER BY promConsumo DESC"

    datosConsumo = consultaBASE(consulta)
    listaId = list()
    listaConsumo = list()
    for x in datosConsumo:
        listaId.append(x[0])
        listaConsumo.append(x[1])

    if(btnValores == 0):
        listaId = listaId[:50]
        listaConsumo = listaConsumo[:50]

    elif(btnValores == 2):
        listaId = listaId[-50:]
        listaConsumo = listaConsumo[-50:]
    data = {'mensaje': "Correcto", "listaId": listaId, "listaConsumo": listaConsumo}

    return JsonResponse(data)

# API cuando el usuario desee ver el consumo de bateria
# usado en estadisticas del app para la grafica que presenta
# el consumo bateria mayor, menor o igual a 50%
def getBateria(_request, idUsuario, btnTiempo):

    listaFechas = list()
    listaBateria = list()
    horaFecha = datetime.now()
    fecha = horaFecha.strftime("%D")
    hora = horaFecha.strftime("%H:%M")

    tiempo = (15, 30, 60)
    tiempo = tiempo[btnTiempo]

    horaFecha = horaFecha - timedelta(minutes = tiempo)

    for x in range(1, tiempo + 1):
        fecha = horaFecha.strftime("%D")
        hora = horaFecha.strftime("%H:%M")
        horaConsulta = fecha + " " + hora
        consulta = "SELECT bateria FROM vehiculos WHERE hora_actual LIKE '"+ horaConsulta + "%' AND id_usuario = '" + idUsuario + "'"
        resultadoConsulta = consultaBASE(consulta)
        print(consulta)
        listaFechas.append(hora)
        listaBateria.append("null" if not resultadoConsulta else resultadoConsulta[0][0])
        horaFecha = horaFecha + timedelta(minutes = 1)

    data = {'mensaje': "Correcto", 'fecha': fecha, "hora": hora, "listaFechas": listaFechas, "listaBateria": listaBateria, "idUsuario": idUsuario}

    return JsonResponse(data)

# API cuando el usuario desee ver el consumo de bateria
# usado en estadisticas del app para la grafica que presenta
# el consumo bateria del uduatio ingresado y por rango de tiempo 
# 30 min, 15 min y 60 min
def getBateriaAhora(_request):
    mas50 = 0
    menos50 = 0
    igual50 = 0
    for x in postAPI():
        if(x['bateria'] > 50):
            mas50 = mas50 + 1
        elif(x['bateria'] < 50):
            menos50 = menos50 + 1
        elif(x['bateria'] == 50):
            igual50 = igual50 + 1

    data = {"mensaje": "Correcto", "mas50": mas50, "menos50": menos50, "igual50": igual50}
    return JsonResponse(data)

# API cuando el usuario desee ver el promedio de velocidades
# usado en control de transito para la grafica que presenta
# el promedio de velocidades segun un rango de fecha
def getVelocidades(_request, fechaMinima, fechaMaxima):
    
    listaVehiculos = list()
    listaVelocidades = list()
    fechaMinimaSeparada = fechaMinima.split("-")
    fechaMaximaSeparada = fechaMaxima.split("-")
    fechaMinimaH = datetime(int(fechaMinimaSeparada[0]), int(fechaMinimaSeparada[1]), int(fechaMinimaSeparada[2]))
    fechaMaximaH = datetime(int(fechaMaximaSeparada[0]), int(fechaMaximaSeparada[1]), int(fechaMaximaSeparada[2]))

    fechaMax = fechaMaximaH.strftime("%D")
    fechaMin = fechaMinimaH.strftime("%D")
    #vManana = 0
    #vTarde = 0
    #vNoche = 0
    listaFechas = list()
    diaNMin = int(fechaMin.split("/")[1])
    diaNMax = int(fechaMax.split("/")[1])

    test = "SELECT id_vehiculo, ROUND(AVG(velocidad), 2) AS velocidades, id_usuario FROM vehiculos WHERE hora_actual LIKE '" + fechaMin + " %' "

    while(diaNMin < diaNMax):

        dia = ""
        if(diaNMin < 9): 

            dia = "0" + str(int(fechaMin.split("/")[1]) + 1)
        else:

            dia = str(int(fechaMin.split("/")[1]) + 1)

        fechaMin = fechaMin.split("/")[0] + "/" + dia + "/" + fechaMin.split("/")[2]
        diaNMin = diaNMin + 1
        listaFechas.append(fechaMin)

    for f in listaFechas:
        test = test + " OR hora_actual LIKE '" + f + " %'"
    
    test = test + "GROUP BY id_vehiculo ORDER BY velocidades DESC"

    valores = consultaBASE(test)
    valores = valores[:12]

    idVehiculos = list()
    velocidades = list()

    for x in valores:
        idVehiculos.append(x[0])
        velocidades.append(x[1])

    data = {'mensaje': "Correcto", "fechaMin": fechaMinima, "fechaMax": fechaMaxima, "Valores": valores, "id_vehiculos": idVehiculos, "velocidades": velocidades}

    return JsonResponse(data)

"""
    * Renderizado de las paginas
"""

# Renderizado de la pagina index
def index(request):
    return render(request, "index.html", {"vehiculosActivos":len(postAPI())})

# Renderizado de la pagina proyecto
def proyecto(request):
    return render(request, "project.html")

#Renderizado de la pagina indicadores
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

# Renderizado de la pagina del login
def login(request):
    return render(request, "login.html")

#Renderizado de los indicadores historicos
def dashboardIndicadoresHistoricos(request):
    return render(request, "dashboardIndicadoresHistoricos.html")

# Renderizado de la pagina de estadisticas
def estadisticas(request):
    avVelocidad = list()
    viasCongestion = list()
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
                    reverse_geocode_result = gmaps.reverse_geocode((vehiculoActual.latitud, vehiculoActual.longitud))
                    try:
                        if(reverse_geocode_result[0]['address_components'][1]['types'] == ['route']):
                            viasCongestion.append(reverse_geocode_result[0]['address_components'][1]['long_name'])
                    except:
                            pass

    if len(viasCongestion) > 10:
        viasCongestion = random.choices(viasCongestion, k=7)

    # Vias centricas con menor congestion 
    viasMenorCongestion = set(viasMenorCongestion)
    avVelocidad = set(avVelocidad)
    viasCongestion = set(viasCongestion)
    if len(viasMenorCongestion) > 10:
        try:
            viasMenorCongestion = random.choices(viasMenorCongestion, k=10)
        except:
            pass

    return render(request, "estadisticas.html", {"avVelocidad": avVelocidad, "viasCongestion": viasCongestion, "viasMenorCongestion": viasMenorCongestion})

# Renderizado del dashboard
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
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eManana = eManana + datosHoras

        for h in range(12,19):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eTarde = eTarde + datosHoras

        for h in range(19,24):
            datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + hora.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
            eNoche = eNoche + datosHoras
        
        eManana = int(eManana / 12)
        eTarde = int(eTarde / 14)
        eNoche = int(eNoche / 10)

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
                datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaFechaActual.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
                eManana = eManana + datosHoras

            for h in range(12,19):
                datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaFechaActual.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
                eTarde = eTarde + datosHoras

            for h in range(19,24):
                datosHoras = Vehiculos.objects.filter(hora_actual__startswith=(fecha + " " + horaFechaActual.replace(hour = h).strftime("%H"))).filter(velocidad__gte=4).filter(velocidad__lt=5).values_list('latitud', 'longitud').distinct().values_list('id_vehiculo').distinct().count()
                eNoche = eNoche + datosHoras
            
            horaFechaActual = horaFechaActual + timedelta(days = 1)
            fecha = horaFechaActual.strftime("%D")
            eManana = int(eManana / 12)
            eTarde = int(eTarde / 14)
            eNoche = int(eNoche / 10)
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

# Renderizado del control de transito
def controlTransito(request):

    datos = postAPI()
    consulta = "SELECT DISTINCT id_vehiculo FROM vehiculos"
    valores = consultaBASE(consulta)
    idVehiculos = list()

    for x in valores:
        idVehiculos.append(x[0])

    return render(request, "controlTransito.html", {"datos": datos, "valores":idVehiculos})

# Renderizado de la pagina de estadisticas del app
def appEstadisticas(request):

    datos = postAPI()
    consulta = "SELECT DISTINCT id_usuario FROM vehiculos"
    valores = consultaBASE(consulta)
    idVehiculos = list()

    for x in valores:
        idVehiculos.append(x[0])

    return render(request, 'appEstadisticas.html', {"valores": idVehiculos})

"""
    * Credenciales para el uso de la base de datos firebase
"""
# Llamo al archivo JSON que contiene mi clave privada
credenciales = credentials.Certificate("serviceAccountKey.json")
# Iniciamos los servicios de Firebase con las credenciales
firebase_admin.initialize_app(credenciales)
db = firestore.client()

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
