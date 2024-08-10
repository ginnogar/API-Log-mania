from flask import Flask, request, jsonify, render_template # Importa las funciones necesarias de Flask.
# Flask crea la aplicación web
# Request maneja las solicitudes entrantes
# Jsonify convierte los datos en formato JSON
# Render_template se utiliza para renderizar plantillas HTML

from flask_sqlalchemy import SQLAlchemy # Importa SQLAlchemy, que es la herramienta que usamos para interactuar con la base de datos.
import datetime # Importa el módulo datetime para manejar fechas y horas en Python.

app = Flask(__name__) # Crea una instancia de la aplicación Flask. 
# __name__ le dice a Flask dónde buscar recursos como plantillas y archivos estáticos.

# Configuración de la base de datos (SQLite en este caso)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db' #Configura la base de datos SQLite, y establece la ubicación del archivo de la base de datos como logs.db.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactiva el seguimiento de modificaciones de objetos de SQLAlchemy para ahorrar recursos, ya que no lo necesitas aquí.

db = SQLAlchemy(app) # Crea una instancia de SQLAlchemy asociada con tu aplicación Flask para manejar la base de datos.

# Modelo de la base de datos para almacenar los logs
class Log(db.Model): # Define un modelo para la tabla Log en la base de datos, que almacena los logs.
    id = db.Column(db.Integer, primary_key=True) # Define una columna id como clave primaria y entero.
    timestamp = db.Column(db.String(50), nullable=False) # Define una columna timestamp para almacenar la hora en que se generó el log como una cadena, y no permite valores nulos.
    service_name = db.Column(db.String(50), nullable=False) # Define una columna service_name para almacenar el nombre del servicio que generó el log, sin permitir valores nulos.
    log_level = db.Column(db.String(20), nullable=False) # Define una columna log_level para almacenar el nivel de log (por ejemplo, INFO, DEBUG), sin permitir valores nulos.
    message = db.Column(db.String(200), nullable=False) # Define una columna message para almacenar el mensaje del log, sin permitir valores nulos.
    received_at = db.Column(db.DateTime, default=datetime.datetime.utcnow) # Define una columna received_at para almacenar la fecha y hora en que el log fue recibido, con un valor por defecto de la hora actual UTC.

# Crear la base de datos
with app.app_context(): # Asegura que las operaciones de la base de datos se realicen dentro del contexto de la aplicación Flask.
    db.create_all() # Crea las tablas en la base de datos basadas en los modelos definidos, en este caso, la tabla Log.

@app.route('/') # Define la ruta para la página principal (/).
def home(): # Define la función home que se ejecuta cuando se visita la página principal.
    return render_template('index.html') # Renderiza la plantilla index.html para mostrarla al usuario.

# Ruta para recibir los logs (POST)
@app.route('/logs', methods=['POST']) # Define una ruta que acepta solicitudes POST en /logs.
def receive_log(): #  Define la función que se ejecuta cuando se recibe un POST en /logs.
    try:
        log_data = request.get_json() # Obtiene los datos JSON enviados en la solicitud POST.

        new_log = Log( # Crea un nuevo registro de log basado en los datos recibidos.
            timestamp=log_data['timestamp'], 
            service_name=log_data['service_name'],
            log_level=log_data['log_level'],
            message=log_data['message']
        )
        db.session.add(new_log) # Añade el nuevo registro a la sesión de la base de datos.
        db.session.commit() # Confirma los cambios, guardando el nuevo registro en la base de datos.

        return jsonify({"message": "Log recibido con exito"}), 201 # 201: Responde al cliente con un mensaje de éxito y un código de estado 201.
    except Exception as e: # Captura cualquier excepción que ocurra.
        return jsonify({"error": "Hubo un error al procesar el log."}), 500 # 500: Responde al cliente con un mensaje de error y un código de estado 500.


# Ruta para obtener los logs (GET) con filtro por fechas
@app.route('/logs', methods=['GET']) # Define una ruta que acepta solicitudes GET en /logs.
def get_logs(): # Define la función que se ejecuta cuando se recibe un GET en /logs.
    start_date_str = request.args.get('start_date') # Obtiene el parámetro start_date de la solicitud.
    end_date_str = request.args.get('end_date') # Obtiene el parámetro end_date de la solicitud.

    try: # Intenta ejecutar el bloque de código.
        if start_date_str: # Verifica si se ha proporcionado start_date.
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M") # Convierte start_date_str en un objeto datetime.
        else: 
            start_date = datetime.datetime.min # Si no se proporciona, usa la fecha mínima.

        if end_date_str: # Verifica si se ha proporcionado end_date.
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M") # Convierte end_date_str en un objeto datetime.
        else:
            end_date = datetime.datetime.max # Si no se proporciona, usa la fecha máxima.

        # Filtrar los logs en base al rango de fechas
        logs = Log.query.filter(Log.received_at >= start_date, Log.received_at <= end_date).all() # Filtra los registros de logs según el rango de fechas.

        logs_list = [ # Crea una lista de diccionarios con la información de los logs filtrados.
            {
                "id": log.id,
                "timestamp": log.timestamp,
                "service_name": log.service_name,
                "log_level": log.log_level,
                "message": log.message,
                "received_at": log.received_at.strftime("%Y-%m-%dT%H:%M:%SZ")
            } for log in logs
        ]

        return jsonify(logs_list), 200 # Crea una lista de diccionarios con la información de los logs filtrados.
    except ValueError as e: # Captura cualquier excepción relacionada con el formato de fecha.
        return jsonify({"error": "Formato de fecha inválido. Use el formato YYYY-MM-DDTHH:MM."}), 400 # Devuelve un mensaje de error si el formato de fecha es incorrecto


if __name__ == '__main__': # Verifica si el archivo se está ejecutando como el script principal.
    app.run(debug=True, port=5001) #  Inicia el servidor Flask en el puerto 5001.
