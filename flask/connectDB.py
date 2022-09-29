from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/fjsaca/Documentos/proyectoGit/LojaRealTime/flask/tempVehiculos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Vehiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    id_usuario = db.Column(db.String)
    id_vehiculo = db.Column(db.String)
    latitud = db.Column(db.String)
    longitud = db.Column(db.String)
    fecha_hora = db.Column(db.String)
    altitud = db.Column(db.String)
    velocidad = db.Column(db.Integer)
    acuri = db.Column(db.String)
    direccion = db.Column(db.String)
    gps = db.Column(db.Integer)
    conexion = db.Column(db.Integer)
    estado = db.Column(db.Integer)
    temperatura = db.Column(db.Integer)
    consumo = db.Column(db.String)
    red = db.Column(db.Integer)
    bateria = db.Column(db.Integer)
    hora_actual = db.Column(db.String)

    def __repr__(self):
        return "<Vehiculo %r" % self.id_vehiculo

if __name__ == "__main__":
    app.run(debug=True)