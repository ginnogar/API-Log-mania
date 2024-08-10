He desarrollado un sistema de monitoreo de logs distribuido. Implementé un servidor central con Flask que recibe, almacena y filtra logs provenientes de distintos servicios. 
Los servicios (servicio1.py y servicio2.py) envían logs periódicamente al servidor central, donde se guardan en una base de datos SQLite. Además, creé una interfaz web (index.html) que permite a los usuarios 
filtrar y visualizar los logs por fecha. También añadí validaciones para las fechas y garantizo la persistencia de los datos recibidos.
