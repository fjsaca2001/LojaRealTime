from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views.generic import View 
import requests
# Importo Firebase Admin SDK 
import firebase_admin

# Hacemos uso de credenciales que nos permitirán usar Firebase Admin SDK 
from firebase_admin import credentials

# Importo el Servicio Cloud Firestore 
from firebase_admin import firestore

def proyecto(request):
    return render(request, "project.html")

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


class Index(View):
    # Especifico la plantilla o template que usaré
    template = "index.html"
    # Llamo al archivo JSON que contiene mi clave privada
    credenciales = credentials.Certificate("serviceAccountKey.json")
    # Iniciamos los servicios de Firebase con las credenciales
    firebase_admin.initialize_app(credenciales)
 
    db = firestore.client()
    #Agrego los valores a la base de datos
    for vehiculo in postAPI():
        db.collection('vehiculos').add(vehiculo)

    def get(self, request):
        return render(request, self.template)


# Login del sistema
def ingreso(request):
    """"
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.data.get("username")
            raw_password = form.data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect(Index)
    else:
        form = AuthenticationForm()

    informacion_template = {'form': form}
    
    return render(request, 'login.html', informacion_template)
    """
    return render(request, 'login.html')
    
# logout del sistema
def logout_view(request):
    """"
    logout(request)
    messages.info(request, "Has salido del sistema")
    """
    return redirect(Index)