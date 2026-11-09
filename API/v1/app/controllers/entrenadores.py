"""Controlador de /api/v1/entrenadores"""
from flask import Blueprint, jsonify, request

from app.index import token_requerido
from app.models.entrenador import Entrenador

entrenadores_bp = Blueprint("entrenadores", __name__)


@entrenadores_bp.get("")
@token_requerido
def listar():
    return jsonify(Entrenador.listar()), 200


@entrenadores_bp.get("/<id>")
@token_requerido
def obtener(id):
    entrenador = Entrenador.obtener(id)
    if entrenador is None:
        return jsonify({"error": "Entrenador no encontrado"}), 404
    return jsonify(entrenador), 200


@entrenadores_bp.post("")
@token_requerido
def crear():
    return jsonify(Entrenador.crear(request.get_json(silent=True))), 201


@entrenadores_bp.put("/<id>")
@token_requerido
def actualizar(id):
    entrenador = Entrenador.actualizar(id, request.get_json(silent=True))
    if entrenador is None:
        return jsonify({"error": "Entrenador no encontrado"}), 404
    return jsonify(entrenador), 200


@entrenadores_bp.delete("/<id>")
@token_requerido
def eliminar(id):
    eliminado, conflicto = Entrenador.eliminar(id)
    if conflicto:
        return jsonify({"error": conflicto}), 409
    if not eliminado:
        return jsonify({"error": "Entrenador no encontrado"}), 404
    return jsonify({"mensaje": "Entrenador eliminado"}), 200
