# Sistema de Gestión de Tareas - API y Cliente

Este proyecto consiste en una API RESTful desarrollada con Flask para la gestión de usuarios y tareas, y un cliente de consola en Python para interactuar con dicha API. Utiliza autenticación basada en tokens JWT y persistencia de datos en una base de datos SQLite.

---
## Características

*   **API RESTful**: Endpoints para el registro y la autenticación de usuarios.
*   **Autenticación**: Utiliza tokens (JWT) para proteger los endpoints. Las contraseñas se almacenan hasheadas `werkzeug`.
*   **Persistencia de Datos**: Usa SQLite gestionado a través del ORM Flask-SQLAlchemy para la manipulación de datos.
*   **Cliente de Consola Interactivo**: Cliente para probar las funcionalidades de la API desde la terminal.
---
## Tecnologías Utilizadas

*   **Backend (API)**:
    *   Python 3.x
    *   Flask
    *   Flask-SQLAlchemy (ORM)
    *   PyJWT (para tokens de autenticación)
    *   Werkzeug (para el hasheo de contraseñas)
*   **Base de Datos**:
    *   SQLite
*   **Cliente**:
    *   Python 3.x
    *   Requests (para realizar peticiones HTTP)

---
## Estructura del Proyecto
```
.
├── app/                  # Directorio principal de la aplicación Flask
│   ├── __init__.py       # Factory de la aplicación (create_app)
│   ├── models.py         # Definición de los modelos de la base de datos (User)
│   └── auth/             # Blueprint para la autenticación y rutas de la API
│       └── routes.py     # Contiene los endpoints /registro, /login, /tareas
│
├── instance/             # Carpeta para archivos de configuración y la base de datos
│   └── tasks.db          # Base de datos SQLite (se crea automáticamente)
│
├── run.py                # Script para iniciar el servidor de la API (para desarrollo)
│
├── cliente.py            # El cliente de consola que interactúa con la API
│
└── README.md
```

---
## Instalación y Configuración


### 1. Prerrequisitos

**Python 3.7** o superior instalado.

### 2. Clonar el Repositorio

```bash
git clone <https://github.com/EmiVargas/flask-tasks-api.git>
```

### 3. Instalar Dependencias

Instala todas las librerías necesarias con el siguiente comando:

```bash
pip install Flask Flask-SQLAlchemy PyJWT Werkzeug requests
```
---
## Uso del Proyecto

Para utilizar la aplicación, necesitas ejecutar el servidor y el cliente en dos terminales separadas.

### 1. Ejecutar el Servidor API

En una terminal, ejecuta el siguiente comando para iniciar el servidor Flask. La base de datos `tasks.db` se creará automáticamente la primera vez.

```bash
python servidor.py
```
Deberías ver una salida indicando que el servidor está corriendo en http://127.0.0.1:5000/.
```bash
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
### 2. Ejecutar el Cliente de Consola
   Abre una nueva terminal (sin cerrar la del servidor) y ejecuta el cliente:

```bash
python cliente.py
```

Aparecerá un menú interactivo:

```bash
===============================
Cliente de Gestión de Tareas
===============================
1. Registrar un nuevo usuario
2. Iniciar sesión
3. Ver mensaje de bienvenida de tareas (requiere sesión)
4. Salir
   Elige una opción:
```

### Ejemplos de Interacción
- Registra un usuario: Elige la opción 1 e introduce un nombre de usuario y una contraseña.
- Inicia sesión: Elige la opción 2 y usa las credenciales que acabas de crear. El cliente guardará el token de sesión.
- Accede a la ruta protegida: Elige la opción 3 para enviar una petición al endpoint /tareas. Como ya has iniciado sesión, el servidor te devolverá un mensaje de bienvenida.
- Salir: Elige la opción 4 para cerrar el cliente.

---

## Endpoints de la API

| Método | Endpoint    | Descripción                                                            | Autenticación |
| :----- | :---------- |:-----------------------------------------------------------------------| :------------ |
| `POST` | `/registro` | Registra un nuevo usuario.                                             | No requerida  |
| `POST` | `/login`    | Autentica a un usuario y devuelve un token JWT.                        | No requerida  |
| `GET`  | `/tareas`   | Devuelve un mensaje de bienvenida si el token es válido.               | Requerida     |
