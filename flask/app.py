from email.policy import default
from time import sleep
from flask import Flask, render_template
import requests
import json
from datetime import datetime
from firebase_admin import credentials, initialize_app, firestore

# Llamo al archivo JSON que contiene mi clave privada
credenciales = credentials.Certificate("/home/fjsaca/Documentos/proyectoGit/LojaRealTime/lojaRealTime/serviceAccountKey.json")
default_app = initialize_app(credenciales)
app = Flask(__name__, template_folder='templates')

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

def createApp():
    #hora.strftime("%D %H:%M:%S")
    hora = datetime.now()
    hora = hora.strftime("%D %H:%M:%S")
    db = firestore.client()
    jsonData = requests.get("http://127.0.0.1:8000/getUbicaciones/")
    vehiculos = json.loads(jsonData.content)['vehiculos']
    print(str(hora))
    for vehiculo in vehiculos:
        vehiculo["hora_actual"] = hora
        db.collection('vehiculos').add(vehiculo)
        #print(vehiculo)

while(True):
    createApp()
