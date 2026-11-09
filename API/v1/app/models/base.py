"""Modelo base con las operaciones CRUD comunes a todas las colecciones.

Cada modelo concreto define:
    coleccion  -> nombre de la colección en MongoDB
    esquema    -> {campo: funcion_conversora}
    requeridos -> campos obligatorios al crear
y puede sobrescribir `reglas` y `motivo_no_eliminar`.
"""
from datetime import datetime, timezone

from pymongo import ReturnDocument

from app.index import a_object_id, get_db


# ---------------------------------------------------------------------------
# Conversores / validadores de campos
# ---------------------------------------------------------------------------
def texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"'{campo}' debe ser un texto no vacío")
    return valor.strip()


def booleano(valor, campo):
    if not isinstance(valor, bool):
        raise ValueError(f"'{campo}' debe ser true o false")
    return valor


def entero_no_negativo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
        raise ValueError(f"'{campo}' debe ser un número entero mayor o igual a 0")
    return valor


def entero_positivo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise ValueError(f"'{campo}' debe ser un número entero mayor a 0")
    return valor


def numero_no_negativo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
        raise ValueError(f"'{campo}' debe ser un número mayor o igual a 0")
    return float(valor)


def object_id(valor, campo):
    return a_object_id(valor, campo)


def fecha(valor, campo):
    if not isinstance(valor, str):
        raise ValueError(f"'{campo}' debe ser una fecha ISO 8601, ej. 2026-10-01T08:00:00Z")
    try:
        resultado = datetime.fromisoformat(valor.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"'{campo}' debe ser una fecha ISO 8601, ej. 2026-10-01T08:00:00Z")
    # MongoDB guarda las fechas en UTC sin zona horaria
    if resultado.tzinfo is not None:
        resultado = resultado.astimezone(timezone.utc).replace(tzinfo=None)
    return resultado


def opcion(*permitidas):
    def validar(valor, campo):
        if valor not in permitidas:
            raise ValueError(f"'{campo}' debe ser uno de: {', '.join(permitidas)}")
        return valor
    return validar


# ---------------------------------------------------------------------------
# Modelo base
# ---------------------------------------------------------------------------
class ModeloBase:
    coleccion = None
    esquema = {}
    requeridos = []

    @classmethod
    def col(cls):
        return get_db()[cls.coleccion]

    # --- Validación ---------------------------------------------------------
    @classmethod
    def validar(cls, datos, parcial=False):
        if not isinstance(datos, dict):
            raise ValueError("El cuerpo de la petición debe ser un objeto JSON")

        no_permitidos = sorted(set(datos) - set(cls.esquema))
        if no_permitidos:
            raise ValueError(f"Campos no permitidos: {', '.join(no_permitidos)}")

        if not parcial:
            faltantes = [c for c in cls.requeridos if c not in datos]
            if faltantes:
                raise ValueError(f"Campos requeridos faltantes: {', '.join(faltantes)}")

        return {campo: cls.esquema[campo](valor, campo) for campo, valor in datos.items()}

    @classmethod
    def reglas(cls, doc, actual=None):
        """Reglas de negocio adicionales. `actual` es el documento existente al actualizar."""

    @classmethod
    def motivo_no_eliminar(cls, oid):
        """Devuelve un mensaje si el documento no puede eliminarse (integridad referencial)."""
        return None

    # --- CRUD ---------------------------------------------------------------
    @classmethod
    def listar(cls):
        return list(cls.col().find())

    @classmethod
    def obtener(cls, id_):
        return cls.col().find_one({"_id": a_object_id(id_)})

    @classmethod
    def crear(cls, datos):
        doc = cls.validar(datos)
        cls.reglas(doc)
        doc["_id"] = cls.col().insert_one(doc).inserted_id
        return doc

    @classmethod
    def actualizar(cls, id_, datos):
        """Actualiza solo los campos enviados. Devuelve None si no existe."""
        oid = a_object_id(id_)
        cambios = cls.validar(datos, parcial=True)
        if not cambios:
            raise ValueError("Debe enviar al menos un campo para actualizar")
        actual = cls.col().find_one({"_id": oid})
        if actual is None:
            return None
        cls.reglas(cambios, actual)
        return cls.col().find_one_and_update(
            {"_id": oid}, {"$set": cambios}, return_document=ReturnDocument.AFTER
        )

    @classmethod
    def eliminar(cls, id_):
        """Devuelve (eliminado: bool, motivo_conflicto: str | None)."""
        oid = a_object_id(id_)
        if cls.col().count_documents({"_id": oid}) == 0:
            return False, None
        motivo = cls.motivo_no_eliminar(oid)
        if motivo:
            return False, motivo
        cls.col().delete_one({"_id": oid})
        return True, None
