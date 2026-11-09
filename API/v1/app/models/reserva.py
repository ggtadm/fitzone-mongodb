"""Modelo de la colección `reservas` (equivale a las "ventas" de pases a clases)."""
from app.index import get_db
from app.models.base import (
    ModeloBase, entero_positivo, fecha, numero_no_negativo, object_id, texto,
)


def clases_reservadas(valor, campo):
    """Valida el arreglo [{clase_id, pases, costo}, ...]."""
    if not isinstance(valor, list) or not valor:
        raise ValueError(f"'{campo}' debe ser una lista con al menos una clase")
    items = []
    for i, item in enumerate(valor):
        prefijo = f"{campo}[{i}]"
        if not isinstance(item, dict):
            raise ValueError(f"'{prefijo}' debe ser un objeto")
        faltantes = [c for c in ("clase_id", "pases", "costo") if c not in item]
        if faltantes:
            raise ValueError(f"'{prefijo}' le faltan campos: {', '.join(faltantes)}")
        extra = sorted(set(item) - {"clase_id", "pases", "costo"})
        if extra:
            raise ValueError(f"'{prefijo}' tiene campos no permitidos: {', '.join(extra)}")
        items.append({
            "clase_id": object_id(item["clase_id"], f"{prefijo}.clase_id"),
            "pases": entero_positivo(item["pases"], f"{prefijo}.pases"),
            "costo": numero_no_negativo(item["costo"], f"{prefijo}.costo"),
        })
    return items


class Reserva(ModeloBase):
    coleccion = "reservas"
    esquema = {
        "miembro_id": object_id,
        "fecha": fecha,
        "clases_reservadas": clases_reservadas,
        "estado_pago": texto,
    }
    requeridos = ["miembro_id", "fecha", "clases_reservadas"]

    @classmethod
    def reglas(cls, doc, actual=None):
        db = get_db()
        if "miembro_id" in doc:
            if db["miembros"].count_documents({"_id": doc["miembro_id"]}) == 0:
                raise ValueError(f"No existe el miembro con id {doc['miembro_id']}")

        if "clases_reservadas" in doc:
            for item in doc["clases_reservadas"]:
                if db["clases"].count_documents({"_id": item["clase_id"]}) == 0:
                    raise ValueError(f"No existe la clase con id {item['clase_id']}")
            # monto_total se calcula siempre en el servidor: suma de pases * costo
            doc["monto_total"] = round(
                sum(i["pases"] * i["costo"] for i in doc["clases_reservadas"]), 2
            )
