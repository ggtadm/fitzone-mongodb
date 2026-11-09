"""Consultas de agregación (vistas/reportes) sobre la colección `reservas`.

Equivalencias con el enunciado:
    marcas  -> entrenadores
    prendas -> clases
    ventas  -> reservas (pases vendidos)
"""
from app.index import get_db

# Etapas reutilizadas: desglosa cada pase reservado y lo une con su clase y entrenador
_RESERVA_CON_CLASE_Y_ENTRENADOR = [
    {"$unwind": "$clases_reservadas"},
    {"$lookup": {
        "from": "clases",
        "localField": "clases_reservadas.clase_id",
        "foreignField": "_id",
        "as": "clase_info",
    }},
    {"$unwind": "$clase_info"},
    {"$lookup": {
        "from": "entrenadores",
        "localField": "clase_info.entrenador_id",
        "foreignField": "_id",
        "as": "entrenador_info",
    }},
    {"$unwind": "$entrenador_info"},
]


class Reporte:

    @staticmethod
    def entrenadores_con_reservas():
        """1. Entrenadores que tienen al menos una reserva (venta)."""
        pipeline = _RESERVA_CON_CLASE_Y_ENTRENADOR + [
            {"$group": {
                "_id": "$entrenador_info._id",
                "entrenador": {"$first": "$entrenador_info.nombre"},
                "especialidad": {"$first": "$entrenador_info.especialidad"},
            }},
            {"$sort": {"entrenador": 1}},
            {"$project": {"_id": 0, "entrenador_id": "$_id", "entrenador": 1, "especialidad": 1}},
        ]
        return list(get_db()["reservas"].aggregate(pipeline))

    @staticmethod
    def clases_cupo_restante():
        """2. Clases reservadas (vendidas) con la cantidad restante de cupo (stock)."""
        pipeline = [
            {"$unwind": "$clases_reservadas"},
            {"$group": {
                "_id": "$clases_reservadas.clase_id",
                "total_pases_vendidos": {"$sum": "$clases_reservadas.pases"},
            }},
            {"$lookup": {
                "from": "clases",
                "localField": "_id",
                "foreignField": "_id",
                "as": "clase_info",
            }},
            {"$unwind": "$clase_info"},
            {"$sort": {"clase_info.nombre": 1}},
            {"$project": {
                "_id": 0,
                "clase_id": "$_id",
                "clase": "$clase_info.nombre",
                "pases_vendidos": "$total_pases_vendidos",
                "cupo_maximo": "$clase_info.cupo_maximo",
                "cupo_actual": "$clase_info.cupo_actual",
                "cupo_restante": {"$subtract": ["$clase_info.cupo_maximo", "$clase_info.cupo_actual"]},
            }},
        ]
        return list(get_db()["reservas"].aggregate(pipeline))

    @staticmethod
    def top_entrenadores(limite=5):
        """3. Los 5 entrenadores con más pases vendidos y su cantidad."""
        pipeline = _RESERVA_CON_CLASE_Y_ENTRENADOR + [
            {"$group": {
                "_id": "$entrenador_info._id",
                "entrenador": {"$first": "$entrenador_info.nombre"},
                "total_pases_vendidos": {"$sum": "$clases_reservadas.pases"},
            }},
            {"$sort": {"total_pases_vendidos": -1, "entrenador": 1}},
            {"$limit": limite},
            {"$project": {"_id": 0, "entrenador_id": "$_id", "entrenador": 1, "total_pases_vendidos": 1}},
        ]
        return list(get_db()["reservas"].aggregate(pipeline))
