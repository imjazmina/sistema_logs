from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timezone

app = Flask(__name__)

DB_NAME = "logs.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id_log INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                service TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                received_at TEXT NOT NULL
            )
        """)
        conn.commit()

def guardar_log(data):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (timestamp, service, severity, message, received_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["timestamp"],
            data["service"],
            data["severity"],
            data["message"],
            datetime.now(timezone.utc).isoformat()  # formato iso 8601 now(timezone.utc)
        ))
        conn.commit()
        return cursor.lastrowid# devuelve el ID de la última fila insertada para verificar que todo ok

#payload: datos que se envían en el cuerpo de una petición HTTP 
def validar_payload(data):
    campos = ["timestamp", "service", "severity", "message"]
    for campo in campos:
        if campo not in data:
            return False, f"Falta el campo: {campo}"
        
    try:
        datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))# validar formato timestamp iso8601 y reemplaza z por 00
    except ValueError:
        return False, "Formato de timestamp inválido"

    # Validar severidad
    if data["severity"] not in ["info", "warning", "error"]:
        return False, "Severidad inválida"

    return True, "OK"

@app.route("/logs", methods=["POST"])
def recibir_logs():
    data = request.get_json()# recibe el json del front

    if not data:
        return jsonify({"error": "Payload vacío"}), 400 # Bad request, servidor no pudo entender la peticion

    logs = data if isinstance(data, list) else [data]#guarda array json u objeto json para manejarlo

    resultados = []
    for log in logs:
        valido, msg = validar_payload(log)
        if valido:
            try:
                log_id = guardar_log(log)
                resultados.append({"status": "ok", "id_log": log_id})
            except Exception as e:
                resultados.append({"status": "error_db", "error": str(e)})
        else:
            resultados.append({"status": "error_validacion", "error": msg, "log": log})

    return jsonify(resultados), 200

@app.route("/logs", methods=["GET"])
def obtener_logs():
    severity = request.args.get("severity")
    service = request.args.get("service")

    query = "SELECT * FROM logs WHERE 1=1" # para ir agregando consultas
    params = []

    if severity:# explain this
        query += " AND severity = ?"
        params.append(severity)

    if service:
        query += " AND service = ?"
        params.append(service)

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    columnas = ["id_log", "timestamp", "service", "severity", "message", "received_at"]
    resultados = [dict(zip(columnas, row)) for row in rows]

    return jsonify(resultados), 200

@app.route("/logs/severity/<valor>", methods=["GET"]) #<valor> variable
def logs_por_severidad(valor):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE severity = ?", (valor,))
        rows = cursor.fetchall()

    columnas = ["id_log", "timestamp", "service", "severity", "message", "received_at"]
    resultados = [dict(zip(columnas, row)) for row in rows]

    return jsonify(resultados), 200

@app.route("/logs/service/<valor>", methods=["GET"])
def logs_por_servicio(valor):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE service = ?", (valor,))
        rows = cursor.fetchall()

    columnas = ["id_log", "timestamp", "service", "severity", "message", "received_at"]
    resultados = [dict(zip(columnas, row)) for row in rows]# recorre todas las filas y las convierte a diccionario

    return jsonify(resultados), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
