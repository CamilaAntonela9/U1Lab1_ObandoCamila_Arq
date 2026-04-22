from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/filtros/validar", methods=["POST"])
def validar():
    datos = request.get_json()
    # Regla: Cédula de 10 dígitos (Paso 4)
    cedula = str(datos.get("cedula", ""))
    if len(cedula) != 10 or not cedula.isdigit():
        return jsonify({"estado": "error", "mensaje": "Cédula inválida (debe tener 10 dígitos)"}), 400
    
    # Regla: Edad (Paso 4)
    edad = datos.get("edad")
    if not isinstance(edad, int) or not (0 <= edad <= 120):
        return jsonify({"estado": "error", "mensaje": "Edad fuera de rango permitido"}), 400
        
    return jsonify({"estado": "ok", "datos": {"datos_validados": True}}), 200

if __name__ == "__main__":
    app.run(port=5002)