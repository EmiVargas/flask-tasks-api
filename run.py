from app import create_app

# Creamos la instancia de la aplicación usando nuestra factory
app = create_app()

if __name__ == '__main__':
    # Ejecutamos la aplicación en modo debug para ver los errores
    app.run(debug=True)