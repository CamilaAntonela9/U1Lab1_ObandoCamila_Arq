from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
ORQUESTADOR_URL = "http://localhost:5001"

@app.route("/api/pacientes/registrar", methods=["POST"])
def registrar_paciente():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400
    try:
        respuesta = requests.post(
            f"{ORQUESTADOR_URL}/pipeline/ejecutar",
            json=datos, timeout=10
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Orquestador no disponible"}), 503

if __name__ == "__main__":
    app.run(port=5000, debug=True)