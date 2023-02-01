# LojaRealTime
El objetivo de este proyecto es, presentar la informacion en tiempo real y de manera historica sobre el trafico e indicadores importantes enfocados al area de movilidad en la ciudada de Loja. 
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
pendiente
## Proyecto Django 
### Configuración
>  Todo lo relacionado con las paginas HTML se han desarrollado con el Framework Django, por ello tambien se realizan las vistas, configuraciones
> y calculos necesarios. Tambien se debe modificar las siguentes direcciones:
- Modificar la direccion que se encuentra dentro de la carpeta lojaRealTime en el archivo settings.py en la linea 59, donde se indica la direccion de los templates del proyecto
- Modificar la direccion que se encuentra dentro de la carpeta lojaRealTime en el archivo settings.py en la linea 81, donde se indica la direccion de la base de datos SQLite
- Modificar la direccion que se encuentra dentro de la carpeta lojaRealTime en el archivo settings.py en la linea 125, donde se indica la direccion de la los archivos etaticos, donde se encuentras lo JS, imagenes, etc. 
### Ejecución
pendiente
