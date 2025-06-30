from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configuración
    app.config['SECRET_KEY'] = 'mi-clave-secreta-para-jwt-y-otros-menesteres'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa extensiones
    db.init_app(app)

    # Importamos los modelos antes de crear la base de datos
    from . import models

    with app.app_context():
        db.create_all()
        print("✅ Base de datos verificada y lista.")

    # Registramos el Blueprint de autenticación
    from .auth.routes import auth_bp
    # Cambiamos el prefijo de URL a la raíz para que las rutas sean /registro y /login
    app.register_blueprint(auth_bp, url_prefix='/')

    return app