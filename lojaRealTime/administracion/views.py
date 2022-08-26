from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View 
# Importo Firebase Admin SDK 
import firebase_admin

# Hacemos uso de credenciales que nos permitirán usar Firebase Admin SDK 
from firebase_admin import credentials

# Importo el Servicio Firebase Realtime Database 
from firebase_admin import db


#def index(request):
 #   return render(request, "index.html", {"nombre": "Joel"})

class Zapatos(View):
    # Especifico la plantilla o template que usaré
    template = "index.html"
    # Llamo al archivo JSON que contiene mi clave privada
    credenciales = credentials.Certificate('./lojarealtime-b480a-firebase-adminsdk-5wpvf-5ab81e1750.json')
    # Iniciamos los servicios de Firebase con las credenciales y el nombre de mi proyecto en Firebase
    firebase_admin.initialize_app(credenciales, {'databaseURL': 'https://lojarealtime-b480a-default-rtdb.firebaseio.com'})
    # Accedo a la base de datos, específicamente a la tabla 'zapatos'
    ref = db.reference('Zapatos')
    ref.set({
        1:{
            'marca': 'adidas',
            'precio': 17.50,
            'talla': 38
        },
        2:{
            'marca': 'puma',
            'precio': 20.00,
            'talla': 40
        },
        3:{
            'marca': 'nike',
            'precio': 90.00,
            'talla': 38
        },
    })
    # Llamo los datos que se encuentran en la tabla 'zapatos'
    datos = ref.get()

    # Envio los datos de la tabla 'postres' a la vista o template 
    def get(self, request):
        return render(request, self.template,{"productos":self.datos})
