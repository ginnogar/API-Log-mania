import requests  # Importa el módulo requests para enviar solicitudes HTTP.
import time      # Importa el módulo time para esperar entre envíos de logs.

# Configuración del servicio
service_name = "Service1"
log_level = "INFO"
message = "Este es un mensaje de informacion"

# URL del servidor central donde se enviarán los logs
url = "http://127.0.0.1:5001/logs"  # Esto es temporal; la URL real dependerá de tu servidor

# API key para la autenticación
api_key = "service1_token"

# Bucle para generar y enviar logs cada 1 hora
while True:
    # Generar el timestamp actual
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    # Crear el log como un diccionario
    log_data = {
        "timestamp": timestamp,
        "service_name": service_name,
        "log_level": log_level,
        "message": message
    }

    # Encabezados para la solicitud HTTP, incluyendo la autenticación
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Enviar el log al servidor central
    response = requests.post(url, json=log_data, headers=headers)

    # Imprimir la respuesta del servidor (para depuración)
    print(f"Log enviado. Respuesta del servidor: {response.status_code}, {response.text}")

    # Esperar 1 minuto (60 segundos) antes de enviar el siguiente log
    time.sleep(60)
