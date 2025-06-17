from app import create_app, db

# Ejecuto create_app() para instanciar en app
app = create_app()

# Si se ejecuta directamente run.py, entonces levanta el servidor de desarrollo de Flask en modo debug
# debug=True habilita --> la recarga en caliente cuando modificas el código y la página de debug cuando ocurre una excepción
if __name__ == "__main__":
    app.run(debug=True)
