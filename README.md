# LojaRealTime
El objetivo de este proyecto es, presentar la informacion en tiempo real y de manera historica sobre el trafico e indicadores importantes enfocados al area de movilidad en la ciudada de Loja. 
## Advertencia
Previo la instalacion y clonacion del repositorio hay que tener en cuentas las siguientes acciones
* Tener instalado la ultima version de Python
* Tener instalado el framework Django
* Tener instalado el framework Flask
## Proyecto Flask 
Al estar trabajando con un API que envia datos constantemente se ha creado una aplicacion que se encarga directamente de almacenar los datos cada cierto tiempo, en este caso 1 min. Esta aplicacion esta desarrollada en flask y esta conectada directamente a la aplicacion Django, ya que mediante un JsonResponse realiza las peticiones al API externo
### Configuración
> La aplicación como ya se menciono solamente matiene la estructura de la base de datos, la clase Vehiculos es la que se 
> encarga de almacenar los datos del Api externa. La configuracion del presente proyecto solo es de modificar las 
> direcciones con las que este cuenta. 
- Modificar la direccion que se encuentra en el archivo app.py en la linea 16, que redirecciona al archivo de configuración serviceAccountKey.json
- Modificar la direccion que se encuentra en el archivo app.py en la linea 39 que permite la obtencion de los datos desde el JsonRepsonse de Django la dirección debera quedar asi: http://rutaProyectoDjango/getUbicaciones/
- Se puede modificar tambien el tiempo de escritura en la base de datos, en la linea 79 del archivo app.py se cambia el tiempo para dormir la escritura
- Modificar la direccion que se encuentra en el archivo connectDB.py en la linea 5, que redirecciona al archivo de conexion a la base de datos de SQLite
### Ejecución
1. Clonar el repositorio
2. Dirigirse al directorio llamado flask, como vemos en la siguiente imagen y podra observar los siguientes archivos. 

![image](https://user-images.githubusercontent.com/49170845/216138507-d096b11a-675e-460a-b7bc-c873b82a64f0.png)
![image](https://user-images.githubusercontent.com/49170845/216139232-045e4d4c-e5b1-4dd6-94d7-08282671bf5b.png)

3. ejecute el siguiente comando

```sh
run flask
```
4. El resultado debe ser algo así

![image](https://user-images.githubusercontent.com/49170845/216138938-6a232829-6597-46e5-8a32-45491bf99d1f.png)

## Proyecto Django 
Todo lo relacionado con las paginas HTML se han desarrollado con el Framework Django, por ello tambien se realizan las vistas, configuraciones y calculos necesarios. Por lo que se considerara el proyecto principal
### Configuración
> A este proyecto solamente se debe modificar las siguentes direcciones de varios archivos ya que al estar en local y pasala a un servidor estas direcciones se veran afectadas. Considerar lo siguiente:
- Modificar la direccion que se encuentra dentro de la carpeta lojaRealTime en el archivo settings.py en la linea 59, donde se indica la direccion de los templates del proyecto
- Modificar la direccion que se encuentra dentro de la carpeta lojaRealTime en el archivo settings.py en la linea 81, donde se indica la direccion de la base de datos SQLite
- Modificar la direccion que se encuentra dentro de la carpeta lojaRealTime en el archivo settings.py en la linea 125, donde se indica la direccion de la los archivos etaticos, donde se encuentras lo JS, imagenes, etc. 
- Modificar la direccion que se encuentra dentro de la carpeta administracion en el archivo views.py en la linea 77, donde se indica la direccion de la base de datos SQLite
### Ejecución
1. Clonar el repositorio
2. Dirigirse al directorio llamado flask, como vemos en la siguiente imagen y podra observar los siguientes archivos. 

![image](https://user-images.githubusercontent.com/49170845/216139721-4099471a-d665-4dc1-ac42-9ed2dbd015f5.png)
![image](https://user-images.githubusercontent.com/49170845/216139504-6a6ba417-f65e-4d4b-996b-9a5fe40322e8.png)

3. ejecute el siguiente comando

```sh
python3 manage.py runserver
```
4. El resultado debe ser algo así

![image](https://user-images.githubusercontent.com/49170845/216139431-ccf32a9b-711c-40fe-a48a-4d9d527a0d4a.png)

# Dirección de la estructura de la BD
[Estructura de la base de datos del proyecto ](https://github.com/fjsaca2001/LojaRealTime/blob/main/flask/tempVehiculos.db.sql)
