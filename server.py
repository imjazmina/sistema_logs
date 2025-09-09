from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# por ahora
logs_almacenados = []

VALID_TOKEN = "Token tokentrue2.0"

def validar_tokens(token):
    return token != VALID_TOKEN

def validar_log_formato(keys):
    formato_logs = {"timestamp", "service", "severity", "message"}
    return formato_logs.issubset(keys)#verificar si todos los elementos de formato_logs están contenidos en keys

@app.route("/logs", methods=["POST"])
def post_logs():
    token = request.headers.get("Authorization")
    if validar_tokens(token):
        return jsonify({"status": "error", "message": "quien sosos"}), 401

    log = request.get_json()
    if not validar_log_formato(log.keys()):
        return jsonify({"status": "error", "message": "Formato invalido"}), 400

    log["received_at"] = datetime.utcnow().isoformat()
    logs_almacenados.append(log)

    return jsonify({
        "status": "success",
        "message": "Log recibido",
        "data": log
    }), 200

@app.route("/logs", methods=["GET"])
def get_logs():
    token = request.headers.get("Authorization")
    if validar_tokens(token):
        return jsonify({"status": "error", "message": "Token inválido"}), 401

    return jsonify({
        "status": "success",
        "logs": logs_almacenados
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
