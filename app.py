import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session
from waitress import serve
import logging
from paste.translogger import TransLogger
from datetime import datetime

# --- Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    stream=sys.stderr
)

logger_wsgi = logging.getLogger('wsgi')
logger_wsgi.setLevel(logging.INFO)

# --- Inicialización de la Aplicación Flask y Configuración
app = Flask(__name__)
app.secret_key = 'clave_secreta_muy_secreta'

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(basedir, 'database', 'Database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Inicialización de la Base de Datos con los Modelos ---

#from models import db, User, Login, Profile
#db.init_app(app)


@app.route('/')
def home():
    return render_template('login.html', logged_in=False)

@app.route('/hotspot-detect.html')
def hotspotiphone():
    
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        # Aquí va la lógica de autenticación que desarrollarás después.
        username = request.form.get('username')
        password = request.form.get('password')

        # Lógica de ejemplo:s
        if username == "user.name" and password == "abc123":
            # Si las credenciales son correctas, el portal cautivo debería
            # autorizar la MAC del dispositivo. Por ahora, solo mostramos un mensaje.
            print(f"Autenticación exitosa para {username}", 'success')
            # Aquí redirigirías a una página de éxito o simplemente devolverías
            # un código que el router entienda como "autorizado".
            return redirect(url_for('main')) 
        else:
            # Si no, se recarga la página de login con un error.
            print('Credenciales incorrectas. Intente de nuevo.', 'error')
            return redirect(url_for('login'))
    
    # Para peticiones GET, simplemente muestra el formulario de login.

    return render_template('login.html')

@app.route('/home')
def main():
    return render_template('home.html', logged_in=False)

@app.route('/logout')
def logout():
    
    #return redirect(url_for('home'))
    return render_template('logout.html')


@app.errorhandler(404)
def page_not_found(e):
    # You can log the error here if you want:
    # app.logger.warning(f"Invalid URL accessed: {request.url} - {e}")
    return render_template('404.html'), 404


# --- Punto de Entrada (sin cambios en la lógica de ejecución) ---
if __name__ == '__main__':
    # logging.getLogger('waitress').setLevel(logging.INFO) # Para logs de waitress
    app_logs = TransLogger(app, setup_console_handler=False) # Translogger para logs de request/response

    # Para desarrollo:
    print("Servidor Flask (debug) iniciando en http://127.0.0.1:80")
    app.run(debug=True, host='127.0.0.1', port=80) # debug=True es solo para desarrollo

    # Para producción (ejemplo con Waitress):
    #print("Servidor Flask (via Waitress) iniciando en http://192.168.10.1:80")
    #serve(app_logs, host='192.168.10.1', port=80, threads=8)