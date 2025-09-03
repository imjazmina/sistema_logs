import random
from datetime import date

mensaje  = ["Inicio de sesion exitosa", "Compra realizada con exito", "Error al crear usuario"]
servicios = ["Inicio sesion", "Alta usuario", "Compra"]
severidad = ["info", "warning", "error"]
fecha = date.today()

token = "fakeToken2.0"

def crear_logs():
    log = {
    "timestamp": fecha.strftime("%d-%m-%Y"),
    "servicio": random.choice(servicios),
    "severity": random.choice(severidad),
    "messaje": random.choice(mensaje)
    }
    return log

crear_logs()