import sys, os
# Asegura que el sistema pueda encontrar la carpeta 'base_de_datos' en la raíz
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from flask import Flask, request, jsonify
# CAMBIO: Ajustado al nombre de tu carpeta 'base_de_datos'
from base_de_datos.db import obtener_conexion 

app = Flask(__name__)

@app.route("/filtros/registrar", methods=["POST"])
def registrar():
    ctx = request.get_json()
    if not ctx:
        return jsonify({"estado": "error", "mensaje": "No se recibieron datos"}), 400
        
    try:
        conn = obtener_conexion()
        if conn is None:
            return jsonify({"estado": "error", "mensaje": "No se pudo conectar a la DB"}), 500
            
        cursor = conn.cursor()
        
        # 1. Verificar duplicados (Cédula es única) [cite: 22, 63]
        cursor.execute("SELECT id FROM pacientes WHERE cedula = %s", (ctx.get("cedula"),))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                "estado": "error", 
                "mensaje": f"Cedula {ctx.get('cedula')} ya registrada"
            }), 400
            
        # 2. Insertar paciente [cite: 22, 196-201]
        cursor.execute(
            """INSERT INTO pacientes (cedula, nombre, apellido, edad, telefono, email) 
               VALUES (%s, %s, %s, %s, %s, %s) 
               RETURNING id, fecha_registro""",
            (
                ctx.get("cedula"), 
                ctx.get("nombre"), 
                ctx.get("apellido"), 
                ctx.get("edad"), 
                ctx.get("telefono"), 
                ctx.get("email")
            )
        )
        
        fila = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "estado": "ok", 
            "mensaje": f"Paciente {ctx.get('nombre')} registrado con éxito",
            "datos": {
                "paciente_id": fila["id"],
                "fecha_registro": str(fila["fecha_registro"])
            }
        }), 200

    except Exception as e:
        return jsonify({"estado": "error", "mensaje": str(e)}), 500
if __name__ == "__main__":
    # Puerto 5003 según el diseño arquitectónico [cite: 26, 173]
    app.run(port=5003, debug=True)