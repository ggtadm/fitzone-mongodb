"""Modelo de la colección `clases`."""
from app.index import get_db
from app.models.base import ModeloBase, entero_no_negativo, entero_positivo, object_id, texto


class Clase(ModeloBase):
    coleccion = "clases"
    esquema = {
        "nombre": texto,
        "entrenador_id": object_id,
        "categoria": texto,
        "cupo_maximo": entero_positivo,
        "cupo_actual": entero_no_negativo,
    }
    requeridos = ["nombre", "entrenador_id", "categoria", "cupo_maximo"]

    @classmethod
    def crear(cls, datos):
        if isinstance(datos, dict):
            datos = {"cupo_actual": 0, **datos}
        return super().crear(datos)

    @classmethod
    def reglas(cls, doc, actual=None):
        if "entrenador_id" in doc:
            if get_db()["entrenadores"].count_documents({"_id": doc["entrenador_id"]}) == 0:
                raise ValueError(f"No existe el entrenador con id {doc['entrenador_id']}")

        actual = actual or {}
        cupo_maximo = doc.get("cupo_maximo", actual.get("cupo_maximo"))
        cupo_actual = doc.get("cupo_actual", actual.get("cupo_actual", 0))
        if cupo_maximo is not None and cupo_actual > cupo_maximo:
            raise ValueError("'cupo_actual' no puede ser mayor que 'cupo_maximo'")

    @classmethod
    def motivo_no_eliminar(cls, oid):
        if get_db()["reservas"].count_documents({"clases_reservadas.clase_id": oid}) > 0:
            return "No se puede eliminar: la clase tiene reservas registradas"
        return None
