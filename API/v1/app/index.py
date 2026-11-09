"""Elementos comunes de la API: conexión a MongoDB, autenticación Bearer y ruta raíz."""
import hmac
from functools import wraps

from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, current_app, jsonify, request
from pymongo import MongoClient

index_bp = Blueprint("index", __name__)


# ---------------------------------------------------------------------------
# Conexión a MongoDB
# ---------------------------------------------------------------------------
def init_db(app):
    """Crea el cliente de MongoDB y guarda la base de datos en la app."""
    cliente = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=5000)
    app.extensions["mongo_db"] = cliente[app.config["MONGO_DB"]]


def get_db():
    return current_app.extensions["mongo_db"]


def a_object_id(valor, campo="id"):
    """Convierte un texto a ObjectId o lanza ValueError con un mensaje claro."""
    if isinstance(valor, ObjectId):
        return valor
    try:
        return ObjectId(valor)
    except (InvalidId, TypeError):
        raise ValueError(f"'{campo}' no es un ObjectId válido: {valor}")


# ---------------------------------------------------------------------------
# Autenticación con Bearer Token
# ---------------------------------------------------------------------------
def token_requerido(f):
    """Exige el encabezado 'Authorization: Bearer <API_TOKEN>'."""

    @wraps(f)
    def envoltura(*args, **kwargs):
        encabezado = request.headers.get("Authorization", "")
        tipo, _, token = encabezado.partition(" ")
        if tipo.lower() != "bearer" or not token.strip():
            return jsonify({"error": "Falta el token. Use 'Authorization: Bearer <token>'"}), 401
        if not hmac.compare_digest(token.strip(), current_app.config["API_TOKEN"]):
            return jsonify({"error": "Token inválido"}), 401
        return f(*args, **kwargs)

    return envoltura


# ---------------------------------------------------------------------------
# Ruta raíz (también protegida con token)
# ---------------------------------------------------------------------------
@index_bp.get("/")
@index_bp.get("/api/v1")
@token_requerido
def index():
    return jsonify({
        "api": "FitZone - Gestión de Gimnasio y Centro Deportivo",
        "version": "v1",
        "recursos": [
            "/api/v1/entrenadores",
            "/api/v1/miembros",
            "/api/v1/clases",
            "/api/v1/reservas",
            "/api/v1/reportes/entrenadores-con-reservas",
            "/api/v1/reportes/clases-cupo-restante",
            "/api/v1/reportes/top-entrenadores",
        ],
        "autenticacion": "Bearer Token en el encabezado Authorization",
    })
