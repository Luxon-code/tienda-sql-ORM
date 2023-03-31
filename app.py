from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

cadenaConexion = "mysql+pymysql://root@localhost/tiendaorm"
app.config["SQLALCHEMY_DATABASE_URI"] = cadenaConexion
app.config["UPLOAD_FOLDER"] = "./static/imagenes" 

db = SQLAlchemy(app)
from controlador.controllerInicio import *
from controlador.controllerProducto import *


if __name__ == "__main__":
    app.run(port=5000,debug=True)