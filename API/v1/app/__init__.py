"""Fábrica de la aplicación Flask de FitZone."""
import os
from datetime import datetime

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider
from pymongo.errors import PyMongoError

from app.index import index_bp, init_db


class MongoJSONProvider(DefaultJSONProvider):
    """Permite devolver ObjectId y fechas de MongoDB en las respuestas JSON."""

    @staticmethod
    def default(o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            texto = o.isoformat()
            return texto + "Z" if o.tzinfo is None else texto
        return DefaultJSONProvider.default(o)


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.json = MongoJSONProvider(app)
    app.json.ensure_ascii = False  # Mostrar tildes y ñ tal cual

    app.config.update(
        MONGO_URI=os.getenv("MONGO_URI", "mongodb://localhost:27017"),
        MONGO_DB=os.getenv("MONGO_DB", "fitzone_db"),
        API_TOKEN=os.getenv("API_TOKEN"),
    )

    if not app.config["API_TOKEN"]:
        raise RuntimeError("Debe definir la variable de entorno API_TOKEN (ver .env.example)")

    init_db(app)

    # Controladores (uno por colección + reportes)
    from app.controllers.entrenadores import entrenadores_bp
    from app.controllers.miembros import miembros_bp
    from app.controllers.clases import clases_bp
    from app.controllers.reservas import reservas_bp
    from app.controllers.reportes import reportes_bp

    prefijo = "/api/v1"
    app.register_blueprint(index_bp)
    app.register_blueprint(entrenadores_bp, url_prefix=f"{prefijo}/entrenadores")
    app.register_blueprint(miembros_bp, url_prefix=f"{prefijo}/miembros")
    app.register_blueprint(clases_bp, url_prefix=f"{prefijo}/clases")
    app.register_blueprint(reservas_bp, url_prefix=f"{prefijo}/reservas")
    app.register_blueprint(reportes_bp, url_prefix=f"{prefijo}/reportes")

    _registrar_errores(app)
    return app


def _registrar_errores(app):
    @app.errorhandler(ValueError)
    def error_validacion(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(404)
    def no_encontrado(_e):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(405)
    def metodo_no_permitido(_e):
        return jsonify({"error": "Método no permitido"}), 405

    @app.errorhandler(PyMongoError)
    def error_mongo(e):
        app.logger.exception(e)
        return jsonify({"error": "Error de conexión con la base de datos"}), 503

    @app.errorhandler(500)
    def error_interno(_e):
        return jsonify({"error": "Error interno del servidor"}), 500
