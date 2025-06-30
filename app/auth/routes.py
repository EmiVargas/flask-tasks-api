import jwt
import datetime
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import User

# Blueprint para la API de autenticación
auth_bp = Blueprint('auth', __name__)

# Decorador para proteger las rutas de la api
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Falta el token de acceso'}), 401

        try:
            # hacemos un decode del token usando la secret key de la app
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'El token ha expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'El token es inválido'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@auth_bp.route('/registro', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('usuario') or not data.get('contraseña'):
        return jsonify({'message': 'Faltan datos (usuario y contraseña son requeridos)'}), 400

    # validar si el usuario ya existe
    if User.query.filter_by(username=data['usuario']).first():
        return jsonify({'message': 'El nombre de usuario ya existe'}), 409

    # como no existe, crea uno nuevo
    user = User(username=data['usuario'])
    user.set_password(data['contraseña'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('usuario') or not data.get('contraseña'):
        return jsonify({'message': 'Faltan datos (usuario y contraseña son requeridos)'}), 400

    user = User.query.filter_by(username=data['usuario']).first()

    # Si el usuario no existe o la contraseña es incorrecta
    if not user or not user.check_password(data['contraseña']):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    # Si pasa la validación devuelvo un JWT
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30) # El token expira en 30 minutos
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token}), 200


@auth_bp.route('/tareas', methods=['GET'])
@token_required
def get_tareas(current_user):
    """
    Ruta de tareas, se valida primero con el decorador @token_required para que accedan usuarios registrados y logeados
    """
    return jsonify({'message': f'¡Bienvenido, {current_user.username}! Listado de tareas: '}), 200