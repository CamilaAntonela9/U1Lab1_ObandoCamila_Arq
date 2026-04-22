from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Definición de la tubería (Pipes)
PIPELINE = [
    {"nombre": "Validador", "url": "http://localhost:5002/filtros/validar"},
    {"nombre": "Registrador", "url": "http://localhost:5003/filtros/registrar"}
]

@app.route("/pipeline/ejecutar", methods=["POST"])
def ejecutar_pipeline():
    contexto = request.get_json()
    historial = []
    
    for filtro in PIPELINE:
        try:
            res = requests.post(filtro["url"], json=contexto, timeout=5)
            resultado = res.json()
            historial.append({"filtro": filtro["nombre"], "resultado": resultado})
            
            if resultado.get("estado") != "ok":
                return jsonify({"estado": "error", "paso": filtro["nombre"], "mensaje": resultado.get("mensaje"), "historial": historial}), 400
            
            # Enriquecimiento del contexto (ADR-002)
            contexto.update(resultado.get("datos", {}))
        except Exception as e:
            return jsonify({"error": f"Fallo en {filtro['nombre']}", "detalle": str(e)}), 503
            
    return jsonify({"estado": "ok", "paciente_id": contexto.get("paciente_id"), "historial": historial}), 200

if __name__ == "__main__":
    app.run(port=5001)