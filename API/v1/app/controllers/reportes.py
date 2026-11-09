"""Controlador de /api/v1/reportes (vistas de solo lectura)."""
from flask import Blueprint, jsonify

from app.index import token_requerido
from app.models.reporte import Reporte

reportes_bp = Blueprint("reportes", __name__)


@reportes_bp.get("/entrenadores-con-reservas")
@token_requerido
def entrenadores_con_reservas():
    """Entrenadores (marcas) con al menos una reserva (venta)."""
    return jsonify(Reporte.entrenadores_con_reservas()), 200


@reportes_bp.get("/clases-cupo-restante")
@token_requerido
def clases_cupo_restante():
    """Clases (prendas) reservadas junto con el cupo (stock) restante."""
    return jsonify(Reporte.clases_cupo_restante()), 200


@reportes_bp.get("/top-entrenadores")
@token_requerido
def top_entrenadores():
    """Top 5 entrenadores (marcas) con más pases vendidos."""
    return jsonify(Reporte.top_entrenadores(5)), 200
