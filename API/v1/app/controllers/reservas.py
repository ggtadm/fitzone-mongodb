"""Controlador de /api/v1/reservas"""
from flask import Blueprint, jsonify, request

from app.index import token_requerido
from app.models.reserva import Reserva

reservas_bp = Blueprint("reservas", __name__)


@reservas_bp.get("")
@token_requerido
def listar():
    return jsonify(Reserva.listar()), 200


@reservas_bp.get("/<id>")
@token_requerido
def obtener(id):
    reserva = Reserva.obtener(id)
    if reserva is None:
        return jsonify({"error": "Reserva no encontrada"}), 404
    return jsonify(reserva), 200


@reservas_bp.post("")
@token_requerido
def crear():
    return jsonify(Reserva.crear(request.get_json(silent=True))), 201


@reservas_bp.put("/<id>")
@token_requerido
def actualizar(id):
    reserva = Reserva.actualizar(id, request.get_json(silent=True))
    if reserva is None:
        return jsonify({"error": "Reserva no encontrada"}), 404
    return jsonify(reserva), 200


@reservas_bp.delete("/<id>")
@token_requerido
def eliminar(id):
    eliminado, _ = Reserva.eliminar(id)
    if not eliminado:
        return jsonify({"error": "Reserva no encontrada"}), 404
    return jsonify({"mensaje": "Reserva eliminada"}), 200
