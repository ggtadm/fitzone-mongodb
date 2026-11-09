"""Controlador de /api/v1/clases"""
from flask import Blueprint, jsonify, request

from app.index import token_requerido
from app.models.clase import Clase

clases_bp = Blueprint("clases", __name__)


@clases_bp.get("")
@token_requerido
def listar():
    return jsonify(Clase.listar()), 200


@clases_bp.get("/<id>")
@token_requerido
def obtener(id):
    clase = Clase.obtener(id)
    if clase is None:
        return jsonify({"error": "Clase no encontrada"}), 404
    return jsonify(clase), 200


@clases_bp.post("")
@token_requerido
def crear():
    return jsonify(Clase.crear(request.get_json(silent=True))), 201


@clases_bp.put("/<id>")
@token_requerido
def actualizar(id):
    clase = Clase.actualizar(id, request.get_json(silent=True))
    if clase is None:
        return jsonify({"error": "Clase no encontrada"}), 404
    return jsonify(clase), 200


@clases_bp.delete("/<id>")
@token_requerido
def eliminar(id):
    eliminado, conflicto = Clase.eliminar(id)
    if conflicto:
        return jsonify({"error": conflicto}), 409
    if not eliminado:
        return jsonify({"error": "Clase no encontrada"}), 404
    return jsonify({"mensaje": "Clase eliminada"}), 200
