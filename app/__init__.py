from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Intancio db pero no la inicializo
db = SQLAlchemy()

# Funcion que configura y deja lista la apliación Flask
def create_app():
    # Creo la aplicación Flask en app
    app = Flask(__name__)
    # URL de conexion a la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Kevin2001@localhost:3306/bd_tienda'
    # Mejora el rendimiento
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Clave secreta para que Flask pueda cifrar la sesion
    app.secret_key = 'una_clave_secreta_que_tu_elijas'

    # Vincula db con la aplicación Flask, y ya se puede usar db en toda la aplicación
    db.init_app(app)

    # Importar modelos para que se registren en SQLAlchemy
    # Importo el modelo Producto
    from app.models.producto import Producto

    # Importe el Blueprint de productos
    # Se registra el Bluepritn en la aplicación con --> app.register_blueprint(productos)
    from .routes.productos import productos
    app.register_blueprint(productos)
    from .routes.carrito import carrito
    app.register_blueprint(carrito)

    # Devulvo la app creada
    return app
