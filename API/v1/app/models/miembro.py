"""Modelo de la colección `miembros`."""
import re

from app.index import get_db
from app.models.base import ModeloBase, booleano, opcion, texto

PLANES = ("Básico", "Mensual", "VIP")
PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def email(valor, campo):
    valor = texto(valor, campo).lower()
    if not PATRON_EMAIL.match(valor):
        raise ValueError(f"'{campo}' no tiene un formato de correo válido")
    return valor


class Miembro(ModeloBase):
    coleccion = "miembros"
    esquema = {
        "nombre": texto,
        "email": email,
        "plan": opcion(*PLANES),
        "activo": booleano,
    }
    requeridos = ["nombre", "email", "plan"]

    @classmethod
    def crear(cls, datos):
        if isinstance(datos, dict):
            datos = {"activo": True, **datos}
        return super().crear(datos)

    @classmethod
    def reglas(cls, doc, actual=None):
        if "email" in doc:
            filtro = {"email": doc["email"]}
            if actual is not None:
                filtro["_id"] = {"$ne": actual["_id"]}
            if cls.col().count_documents(filtro) > 0:
                raise ValueError(f"Ya existe un miembro con el email {doc['email']}")

    @classmethod
    def motivo_no_eliminar(cls, oid):
        if get_db()["reservas"].count_documents({"miembro_id": oid}) > 0:
            return "No se puede eliminar: el miembro tiene reservas registradas"
        return None
