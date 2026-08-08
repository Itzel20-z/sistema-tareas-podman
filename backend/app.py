import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Tarea

app = Flask(__name__)
CORS(app)  # permite que el frontend (otro origen/puerto) consuma la API

# --- Configuración de base de datos vía variables de entorno ---
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "db")          # nombre del contenedor de la BD
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "tareas_db")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

ESTADOS_VALIDOS = {"pendiente", "en_proceso", "completada"}
PRIORIDADES_VALIDAS = {"baja", "media", "alta"}


@app.route("/api/health", methods=["GET"])
def health():
    """Endpoint simple para verificar que la API está viva."""
    return jsonify({"status": "ok"}), 200


# ---------- CRUD: Crear ----------
@app.route("/api/tareas", methods=["POST"])
def crear_tarea():
    datos = request.get_json(silent=True) or {}

    titulo = datos.get("titulo", "").strip()
    if not titulo:
        return jsonify({"error": "El campo 'titulo' es obligatorio"}), 400

    estado = datos.get("estado", "pendiente")
    if estado not in ESTADOS_VALIDOS:
        return jsonify({"error": f"estado inválido, use uno de {ESTADOS_VALIDOS}"}), 400

    prioridad = datos.get("prioridad", "media")
    if prioridad not in PRIORIDADES_VALIDAS:
        return jsonify({"error": f"prioridad inválida, use una de {PRIORIDADES_VALIDAS}"}), 400

    fecha_limite = None
    if datos.get("fecha_limite"):
        try:
            fecha_limite = datetime.strptime(datos["fecha_limite"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "fecha_limite debe tener formato YYYY-MM-DD"}), 400

    nueva_tarea = Tarea(
        titulo=titulo,
        descripcion=datos.get("descripcion", ""),
        estado=estado,
        prioridad=prioridad,
        fecha_limite=fecha_limite,
    )
    db.session.add(nueva_tarea)
    db.session.commit()
    return jsonify(nueva_tarea.to_dict()), 201


# ---------- CRUD: Leer todas (con filtros opcionales) ----------
@app.route("/api/tareas", methods=["GET"])
def listar_tareas():
    query = Tarea.query

    estado = request.args.get("estado")
    if estado:
        query = query.filter_by(estado=estado)

    prioridad = request.args.get("prioridad")
    if prioridad:
        query = query.filter_by(prioridad=prioridad)

    tareas = query.order_by(Tarea.fecha_creacion.desc()).all()
    return jsonify([t.to_dict() for t in tareas]), 200


# ---------- CRUD: Leer una ----------
@app.route("/api/tareas/<int:tarea_id>", methods=["GET"])
def obtener_tarea(tarea_id):
    tarea = Tarea.query.get(tarea_id)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(tarea.to_dict()), 200


# ---------- CRUD: Actualizar ----------
@app.route("/api/tareas/<int:tarea_id>", methods=["PUT"])
def actualizar_tarea(tarea_id):
    tarea = Tarea.query.get(tarea_id)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    datos = request.get_json(silent=True) or {}

    if "titulo" in datos:
        if not datos["titulo"].strip():
            return jsonify({"error": "El título no puede estar vacío"}), 400
        tarea.titulo = datos["titulo"].strip()

    if "descripcion" in datos:
        tarea.descripcion = datos["descripcion"]

    if "estado" in datos:
        if datos["estado"] not in ESTADOS_VALIDOS:
            return jsonify({"error": f"estado inválido, use uno de {ESTADOS_VALIDOS}"}), 400
        tarea.estado = datos["estado"]

    if "prioridad" in datos:
        if datos["prioridad"] not in PRIORIDADES_VALIDAS:
            return jsonify({"error": f"prioridad inválida, use una de {PRIORIDADES_VALIDAS}"}), 400
        tarea.prioridad = datos["prioridad"]

    if "fecha_limite" in datos:
        if datos["fecha_limite"]:
            try:
                tarea.fecha_limite = datetime.strptime(datos["fecha_limite"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "fecha_limite debe tener formato YYYY-MM-DD"}), 400
        else:
            tarea.fecha_limite = None

    db.session.commit()
    return jsonify(tarea.to_dict()), 200


# ---------- CRUD: Eliminar ----------
@app.route("/api/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.get(tarea_id)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    db.session.delete(tarea)
    db.session.commit()
    return jsonify({"mensaje": "Tarea eliminada correctamente"}), 200


def crear_tablas_si_no_existen():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    crear_tablas_si_no_existen()
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    # También crea las tablas cuando se ejecuta con un servidor WSGI (gunicorn)
    crear_tablas_si_no_existen()
