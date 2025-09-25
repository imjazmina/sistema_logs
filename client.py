import random
import requests
from datetime import datetime, timezone
import time

url_server = "http://127.0.0.1:5000/post-logs" #definir endpoint para recuperar datos, mi servidor

servicios = ["Inicio sesion", "Alta usuario", "Compra"]
severidad = ["info", "warning", "error"]

def crear_logs():
    log = {
    "timestamp": datetime.now(timezone.utc).isoformat(),#fecha y hora que se envio
    "service": random.choice(servicios),
    "severity": random.choice(severidad),
    "message": "This is the log we created."
    }
    return log

def enviar_logs(cantidad, delay= 1):
        
    for i in range(cantidad):
        log = crear_logs()
        try:
            r = requests.post(#envia el json de loggssss
                url_server, 
                json=log,#Para indicar a la API que estamos enviando explícitamente un objeto JSON a la URL especificada. 
                headers={"Authorization": "fakeToken2.0"} #agrega un header al dicc
            )
            if r.status_code == 200:#si la respuesta es exitosa
                print(f"Log enviado {r.status_code} : {r.json()}")#para almacenar los datos de la respuesta en un objeto diccionario
            else:
                print(f"Error al enviar el log {r.status_code} : {r.json()}")
        except Exception as e:
            print(f"Error de conexion {e}")
        time.sleep(delay)

if __name__ == "__main__":
    enviar_logs(cantidad=5)