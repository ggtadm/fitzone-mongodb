"""Modelo de la colección `entrenadores`."""
from app.index import get_db
from app.models.base import ModeloBase, booleano, texto


class Entrenador(ModeloBase):
    coleccion = "entrenadores"
    esquema = {
        "nombre": texto,
        "especialidad": texto,
        "activo": booleano,
    }
    requeridos = ["nombre", "especialidad"]

    @classmethod
    def crear(cls, datos):
        if isinstance(datos, dict):
            datos = {"activo": True, **datos}
        return super().crear(datos)

    @classmethod
    def motivo_no_eliminar(cls, oid):
        if get_db()["clases"].count_documents({"entrenador_id": oid}) > 0:
            return "No se puede eliminar: el entrenador tiene clases asignadas"
        return None
