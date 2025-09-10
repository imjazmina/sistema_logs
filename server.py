from flask import Flask, request, jsonify
from datetime import datetime, timezone
import sqlite3

app = Flask(__name__)

# por ahora
logs_almacenados = []

#tokens por servicio
true_tokens ={
    "inicio_sesion": "123",
    "pagos": "456",
    "notificaciones": "789"
} 

def validar_tokens(token):
    return token in true_tokens.values()

def validar_log_formato(keys):
    formato_logs = {"timestamp", "service", "severity", "message"}
    return formato_logs.issubset(keys)#verificar si todos los elementos de formato_logs están contenidos en keys

def conexion_db():
    conn = sqlite3.connect("logs.db")
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_db():
    conn = conexion_db()
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
    conn.close()

#enviar json a base de datos
@app.route("/post-logs", methods=["POST"])
def post_logs():
    #get requets
    log = request.get_json()
    token = request.headers.get("Authorization")

    if not validar_log_formato(log.keys()):
        return jsonify({"status": "error", "message": "Formato invalido"}), 400
    
    log["received_at"] = datetime.now(timezone.utc).isoformat()
    try:
        conn = conexion_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (timestamp, service, severity, message, received_at) VALUES (?, ?, ?, ?, ?)",
            (log["timestamp"], log["service"], log["severity"], log["message"], log["received_at"])
        )
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"status": "error", "message": f"{e}"}), 400

    if not validar_tokens(token):
        return jsonify({"status": "error", "message": "quien sos broer"}), 401
    
    return jsonify({
        "status": "success",
        "message": "Log recibido",
        "data": log
    }), 200

# filtrado logs por hora recibida
@app.route("/recibidos", methods=["GET"])
def recieved_logs():
    conn = conexion_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY received_at DESC")
    rows = cursor.fetchall()
    conn.close()

    logs = [dict(row) for row in rows]

    return jsonify({
        "status": "success",
        "logs": logs
    }), 200

# filtrado todos los logs
@app.route("/all-logs", methods=["GET"])
def get_all_logs():
    conn = conexion_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    logs = [dict(row) for row in rows]

    return jsonify({
        "status": "success",
        "logs": logs
    }), 200

# filtrado todos los logs por hora recibida
@app.route("/logs", methods=["GET"])
def get_logs():
    conn = conexion_db()
    cursor = conn.cursor()
    cursor.execute("SELECT service FROM logs ORDER BY service ASC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    logs = [dict(row) for row in rows]

    return jsonify({
        "status": "success",
        "logs": logs
    }), 200


if __name__ == "__main__":
    inicializar_db()
    app.run(debug=True)
