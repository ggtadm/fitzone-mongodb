"""Controlador de /api/v1/miembros"""
from flask import Blueprint, jsonify, request

from app.index import token_requerido
from app.models.miembro import Miembro

miembros_bp = Blueprint("miembros", __name__)


@miembros_bp.get("")
@token_requerido
def listar():
    return jsonify(Miembro.listar()), 200


@miembros_bp.get("/<id>")
@token_requerido
def obtener(id):
    miembro = Miembro.obtener(id)
    if miembro is None:
        return jsonify({"error": "Miembro no encontrado"}), 404
    return jsonify(miembro), 200


@miembros_bp.post("")
@token_requerido
def crear():
    return jsonify(Miembro.crear(request.get_json(silent=True))), 201


@miembros_bp.put("/<id>")
@token_requerido
def actualizar(id):
    miembro = Miembro.actualizar(id, request.get_json(silent=True))
    if miembro is None:
        return jsonify({"error": "Miembro no encontrado"}), 404
    return jsonify(miembro), 200


@miembros_bp.delete("/<id>")
@token_requerido
def eliminar(id):
    eliminado, conflicto = Miembro.eliminar(id)
    if conflicto:
        return jsonify({"error": conflicto}), 409
    if not eliminado:
        return jsonify({"error": "Miembro no encontrado"}), 404
    return jsonify({"mensaje": "Miembro eliminado"}), 200
