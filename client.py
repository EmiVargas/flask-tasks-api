import requests
import json

# URL base de nuestra API. Asegúrate de que el servidor (run.py) esté corriendo.
API_URL = "http://127.0.0.1:5000"

# Esta variable guardará el token JWT para usarlo en las peticiones protegidas.
# Es una variable global simple, suficiente para este cliente de consola.
token_jwt = None

def registrar_usuario():
    """Pide datos y los envía al endpoint /registro de la API."""
    print("\n--- Registro de Nuevo Usuario ---")
    usuario = input("Elige un nombre de usuario: ")
    contraseña = input("Elige una contraseña: ")

    # El payload debe coincidir con lo que espera la API
    payload = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    try:
        # Hacemos la petición POST
        response = requests.post(f"{API_URL}/registro", json=payload)

        # requests.raise_for_status() lanzará un error si el código de estado es 4xx o 5xx
        response.raise_for_status()

        # Mostramos la respuesta del servidor (si todo fue bien)
        print("\n✅ Respuesta del servidor:", response.json()['message'])

    except requests.exceptions.HTTPError as err:
        # Si la API devuelve un error (ej. usuario ya existe), lo mostramos
        print(f"\n❌ Error de registro: {err.response.json()['message']}")
    except requests.exceptions.RequestException as err:
        # Para otros errores como problemas de conexión
        print(f"\n❌ Error de conexión: {err}")


def iniciar_sesion():
    """Pide credenciales, las envía a /login y guarda el token."""
    global token_jwt # Indicamos que vamos a modificar la variable global

    print("\n--- Inicio de Sesión ---")
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    payload = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    try:
        response = requests.post(f"{API_URL}/login", json=payload)
        response.raise_for_status()

        # Si el login es exitoso, guardamos el token
        token_jwt = response.json()['token']
        print("\n✅ Inicio de sesión exitoso. ¡Token guardado!")

    except requests.exceptions.HTTPError as err:
        print(f"\n❌ Error de inicio de sesión: {err.response.json()['message']}")
    except requests.exceptions.RequestException as err:
        print(f"\n❌ Error de conexión: {err}")


def ver_tareas():
    """Envía una petición a /tareas usando el token guardado."""
    global token_jwt

    print("\n--- Obteniendo Bienvenida de Tareas ---")

    if not token_jwt:
        print("\n⚠️ Debes iniciar sesión primero para ver esta sección.")
        return

    # Las cabeceras (headers) son donde enviamos información adicional, como el token
    headers = {
        "x-access-token": token_jwt
    }

    try:
        response = requests.get(f"{API_URL}/tareas", headers=headers)
        response.raise_for_status()

        print("\n✅ Respuesta del servidor:", response.json()['message'])

    except requests.exceptions.HTTPError as err:
        print(f"\n❌ Error al obtener las tareas: {err.response.json()['message']}")
    except requests.exceptions.RequestException as err:
        print(f"\n❌ Error de conexión: {err}")

def mostrar_menu():
    """Muestra el menú principal y gestiona la elección del usuario."""
    while True:
        print("\n===============================")
        print("   Cliente de Gestión de Tareas")
        print("===============================")
        print("1. Registrar un nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Ver mensaje de bienvenida de tareas (requiere sesión)")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            iniciar_sesion()
        elif opcion == '3':
            ver_tareas()
        elif opcion == '4':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

# --- Punto de entrada del script ---
if __name__ == "__main__":
    mostrar_menu()