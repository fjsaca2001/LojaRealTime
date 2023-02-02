from email.policy import default
from time import sleep
from flask import Flask, render_template
import requests
import json
from datetime import datetime
from firebase_admin import credentials, initialize_app, firestore
from connectDB import Vehiculos
from connectDB import db
from flask_sqlalchemy import SQLAlchemy
#import googlemaps
from geopy.geocoders import Nominatim


# Llamo al archivo JSON que contiene mi clave privada
credenciales = credentials.Certificate("/home/fjsaca/Documentos/proyectoGit/LojaRealTime/lojaRealTime/serviceAccountKey.json")
default_app = initialize_app(credenciales)
app = Flask(__name__, template_folder='templates')
"""
@app.route("/")
        
def index():
    return render_template("index.html")
@app.route("/casa")
def casa():
    r = requests.get("http://127.0.0.1:8000/getUbicaciones/")
    casa = json.loads(r.content)['vehiculos']
    datos2 = []
    for d in casa:
         datos2.append({'id_usuario': d['id_usuario'] ,  'velocidad':d['velocidad'] })
    return render_template("casa.html", casa=datos2)
"""

def createApp():
    #hora.strftime("%D %H:%M:%S")
    hora = datetime.now()
    hora = hora.strftime("%D %H:%M:%S")
    #db2 = firestore.client()
    jsonData = requests.get("http://127.0.0.1:8000/getUbicaciones/")
    vehiculos = json.loads(jsonData.content)['vehiculos']
    print("Escrito a las: " + str(hora))
    #gmaps = googlemaps.Client(key='AIzaSyBmcEHbItWXSbgIH8BiQuD6Ns5bfyBoLtY')
    geolocalizador = Nominatim(user_agent="appLoja")

    for vehiculo in vehiculos:
        #reverse_geocode_result = gmaps.reverse_geocode((vehiculo["latitud"], vehiculo["longitud"]))
        ubicacion = ""
        """if(vehiculo["velocidad"] > 5):
            try:
                ubicacion = (geolocalizador.reverse((vehiculo["latitud"], vehiculo["longitud"]))).raw['address']['road']
            except:
                ubicacion = """""
        vehiculo["hora_actual"] = hora
        newVehiculo = Vehiculos(
            id_usuario = vehiculo["id_usuario"],
            id_vehiculo =  vehiculo["id_vehiculo"],
            latitud =  vehiculo["latitud"],
            longitud =  vehiculo["longitud"],
            fecha_hora =  vehiculo["fecha_hora"],
            altitud =  vehiculo["altitud"],
            velocidad =  vehiculo["velocidad"],
            acuri =  vehiculo["acuri"],
            direccion =  vehiculo["direccion"],
            gps =  vehiculo["gps"],
            conexion =  vehiculo["conexion"],
            estado =  vehiculo["estado"],
            temperatura =  vehiculo["temperatura"],
            consumo =  vehiculo["consumo"],
            red =  vehiculo["red"],
            bateria =  vehiculo["bateria"],
            hora_actual =  vehiculo["hora_actual"],
            #ubicacion = reverse_geocode_result[0]["formatted_address"]
            #ubicacion = ubicacion
        )
        db.session.add(newVehiculo)
    db.session.commit()
    print("Ejecucion Dormida")
    #sleep(348)
    sleep(58)
while(True):
    createApp()
