# Sistema de Gestión para FitZone (Gimnasio y Centro Deportivo)

Este proyecto consiste en la creación de una **base de datos NoSQL con MongoDB** para un centro deportivo y gimnasio, permitiendo la gestión de miembros, entrenadores, clases grupales y el registro de reservas/asistencias.



 👤 Miembros
```json
{
  "_id": "60d5ecb8b5c9c22b1c8e0201",
  "nombre": "Sonia Araya",
  "email": "sonia@example.com",
  "plan": "VIP",
  "activo": true
}
```

 🏋️ Entrenadores
```json
{
  "_id": "60d5ecb8b5c9c22b1c8e0101",
  "nombre": "Carlos Ruiz",
  "especialidad": "CrossFit",
  "activo": true
}
```

 🧘 Clases
```json
{
  "_id": "60d5ecb8b5c9c22b1c8e0301",
  "nombre": "CrossFit Matutino",
  "entrenador_id": "60d5ecb8b5c9c22b1c8e0101",
  "categoria": "Alta Intensidad",
  "cupo_maximo": 15,
  "cupo_actual": 10
}
```

🎟️ Reservas
```json
{
  "_id": "60d5ecb8b5c9c22b1c8e0401",
  "miembro_id": "60d5ecb8b5c9c22b1c8e0201",
  "fecha": "2026-10-01T08:00:00.000Z",
  "clases_reservadas": [
    {
      "clase_id": "60d5ecb8b5c9c22b1c8e0301",
      "pases": 1,
      "costo": 10.00
    },
    {
      "clase_id": "60d5ecb8b5c9c22b1c8e0303",
      "pases": 1,
      "costo": 12.00
    }
  ],
  "monto_total": 22.00
}
```
---

# 🌐 API REST de FitZone (Python + Flask)

API REST con arquitectura en capas (**controladores** y **modelos** por colección) conectada a MongoDB, con CRUD completo para cada colección, autenticación **Bearer Token** y endpoints de reportes.

## 📁 Estructura

```
API/
├── FitZone.postman_collection.json            # Colección de Postman (flujo completo con tests)
├── FitZone.postman_environment.example.json   # Entorno de Postman de ejemplo (base_url, token)
└── v1/
    ├── run.py                  # Punto de entrada
    ├── requirements.txt
    ├── .env.example            # Variables de entorno de ejemplo
    └── app/
        ├── __init__.py         # Fábrica de la app, registro de rutas y errores
        ├── index.py            # Conexión a MongoDB, autenticación Bearer y ruta raíz
        ├── controllers/        # Capa de controladores (rutas HTTP)
        │   ├── entrenadores.py
        │   ├── miembros.py
        │   ├── clases.py
        │   ├── reservas.py
        │   └── reportes.py
        └── models/             # Capa de modelos (acceso a MongoDB y validaciones)
            ├── base.py         # CRUD y validaciones comunes
            ├── entrenador.py
            ├── miembro.py
            ├── clase.py
            ├── reserva.py
            └── reporte.py      # Consultas de agregación
```

## ▶️ Instalación y ejecución

1. Cargar los datos en el cluster de **MongoDB Atlas** ejecutando [database/script.mongodb.js](database/script.mongodb.js) con la extensión MongoDB for VS Code (también funciona con un MongoDB local).
   > ⚠️ El script hace `drop()` de las colecciones: volver a ejecutarlo borra los datos creados desde la API.
2. Instalar dependencias y configurar el entorno:
   ```bash
   cd API/v1
   python -m venv venv
   venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
   pip install -r requirements.txt
   copy .env.example .env         # Linux/Mac: cp .env.example .env
   ```
3. Editar `.env`:
   - `MONGO_URI`: cadena de conexión de Atlas (`mongodb+srv://usuario:contraseña@clusterggt.jlkgst3.mongodb.net/...`), obtenida en **Atlas → Connect → Drivers**.
   - `MONGO_DB`: `fitzone_db`.
   - `API_TOKEN`: el token que usarán los clientes.

   En Atlas, la IP de la computadora debe estar permitida en **Network Access**.
4. Iniciar la API:
   ```bash
   python run.py
   ```
   La API queda disponible en `http://127.0.0.1:5000/api/v1`.

## 🧪 Pruebas con Postman

1. Iniciar la API (`python run.py`). Si se cambia el `.env`, **hay que detener y volver a iniciar la API** para que tome los valores nuevos.
2. En Postman: **Import** → seleccionar:
   - [API/FitZone.postman_collection.json](API/FitZone.postman_collection.json) (colección), y
   - `API/FitZone.postman_environment.json` (entorno con `base_url` y `token`; no se sube a git porque contiene el token). Si no existe, importar [API/FitZone.postman_environment.example.json](API/FitZone.postman_environment.example.json) y colocar en `token` el valor de `API_TOKEN` del `.env`.
3. Seleccionar el entorno **FitZone Local** (arriba a la derecha en Postman).
4. Clic derecho en la colección → **Run collection** → **Run FitZone API v1**.

La colección funciona incluso con la base vacía. Las carpetas se ejecutan en orden:

| Carpeta | Qué prueba |
|---|---|
| 1–4. Entrenadores, Miembros, Clases, Reservas | Crea un registro de prueba en cada colección (guarda su `_id` en una variable) y lo consulta y actualiza |
| 5. Reportes | Los tres reportes de agregación |
| 6. Validaciones | Errores esperados: 400 (campos faltantes, valores inválidos, email repetido, cupo excedido), 404 y 409 (integridad referencial) |
| 7. Limpieza | Elimina los registros de prueba, así la base queda como estaba |
| 8. Seguridad | Sin token y con token inválido → 401 |

Cada petición tiene tests (código de estado, respuesta JSON, valores devueltos) que se ven en la pestaña **Test Results**.

## 🔐 Autenticación

**Todas** las peticiones requieren el encabezado:

```
Authorization: Bearer <API_TOKEN>
```

En Postman: pestaña **Authorization** → Type **Bearer Token** → colocar el token (la colección ya lo trae configurado con la variable `{{token}}`).

Si el token falta o es incorrecto, la API responde:

```json
// 401 Unauthorized
{ "error": "Token inválido" }
```

## 📌 Convenciones

- URL base: `http://127.0.0.1:5000/api/v1`
- Cuerpo de las peticiones y respuestas en **JSON** (`Content-Type: application/json`).
- `{id}` es el `_id` de MongoDB (ObjectId de 24 caracteres hexadecimales).
- **PUT** actualiza solo los campos enviados (los demás se conservan).
- Códigos de respuesta:

| Código | Significado |
|--------|-------------|
| 200 | Operación exitosa |
| 201 | Recurso creado |
| 400 | Datos inválidos, campos faltantes/no permitidos o id mal formado |
| 401 | Token ausente o inválido |
| 404 | Recurso no encontrado |
| 409 | No se puede eliminar porque otros documentos dependen de él |
| 503 | No hay conexión con MongoDB |

Ejemplo de error de validación (400):
```json
{ "error": "Campos requeridos faltantes: entrenador_id, categoria, cupo_maximo" }
```

## 🏠 Información de la API

**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1`

Devuelve el nombre de la API y la lista de recursos disponibles.

---

## 🏋️ Entrenadores

| Campo | Tipo | Requerido (POST) | Descripción |
|-------|------|:---:|-------------|
| `nombre` | string | ✅ | Nombre completo |
| `especialidad` | string | ✅ | Ej. CrossFit, Yoga, Spinning |
| `activo` | boolean | ❌ | Por defecto `true` |

### Obtener todos los entrenadores
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/entrenadores`

**Respuesta (200):**
```json
[
  { "_id": "60d5ecb8b5c9c22b1c8e0101", "nombre": "Carlos Ruiz", "especialidad": "CrossFit & High Intensity", "activo": true },
  { "_id": "60d5ecb8b5c9c22b1c8e0102", "nombre": "Ana Morales", "especialidad": "Yoga", "activo": true }
]
```

### Obtener entrenador por ID
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/entrenadores/{id}`
**Ejemplo:** `http://127.0.0.1:5000/api/v1/entrenadores/60d5ecb8b5c9c22b1c8e0101`

**Respuesta (200):**
```json
{ "_id": "60d5ecb8b5c9c22b1c8e0101", "nombre": "Carlos Ruiz", "especialidad": "CrossFit & High Intensity", "activo": true }
```
Si no existe: `404` → `{ "error": "Entrenador no encontrado" }`

### Insertar entrenador
**Método:** `POST`
**URL:** `http://127.0.0.1:5000/api/v1/entrenadores`

**Body:**
```json
{ "nombre": "Pedro Jiménez", "especialidad": "Funcional" }
```
**Respuesta (201):**
```json
{ "_id": "6650f1a2c3d4e5f6a7b8c901", "nombre": "Pedro Jiménez", "especialidad": "Funcional", "activo": true }
```

### Actualizar entrenador
**Método:** `PUT`
**URL:** `http://127.0.0.1:5000/api/v1/entrenadores/{id}`

**Body** (solo los campos a modificar):
```json
{ "especialidad": "Funcional y TRX", "activo": false }
```
**Respuesta (200):** el entrenador con los cambios aplicados.

### Eliminar entrenador
**Método:** `DELETE`
**URL:** `http://127.0.0.1:5000/api/v1/entrenadores/{id}`

**Respuesta (200):**
```json
{ "mensaje": "Entrenador eliminado" }
```
Si el entrenador tiene clases asignadas: `409` → `{ "error": "No se puede eliminar: el entrenador tiene clases asignadas" }`

---

## 👤 Miembros

| Campo | Tipo | Requerido (POST) | Descripción |
|-------|------|:---:|-------------|
| `nombre` | string | ✅ | Nombre completo |
| `email` | string | ✅ | Correo válido y único |
| `plan` | string | ✅ | `Básico`, `Mensual` o `VIP` |
| `activo` | boolean | ❌ | Por defecto `true` |

### Obtener todos los miembros
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/miembros`

**Respuesta (200):**
```json
[
  { "_id": "60d5ecb8b5c9c22b1c8e0201", "nombre": "Sonia Araya", "email": "sonia@example.com", "plan": "VIP", "activo": true },
  { "_id": "60d5ecb8b5c9c22b1c8e0202", "nombre": "Roberto Méndez", "email": "roberto@example.com", "plan": "VIP", "activo": true }
]
```

### Obtener miembro por ID
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/miembros/{id}`
**Ejemplo:** `http://127.0.0.1:5000/api/v1/miembros/60d5ecb8b5c9c22b1c8e0201`

**Respuesta (200):**
```json
{ "_id": "60d5ecb8b5c9c22b1c8e0201", "nombre": "Sonia Araya", "email": "sonia@example.com", "plan": "VIP", "activo": true }
```
Si no existe: `404` → `{ "error": "Miembro no encontrado" }`

### Insertar miembro
**Método:** `POST`
**URL:** `http://127.0.0.1:5000/api/v1/miembros`

**Body:**
```json
{ "nombre": "Lucía Herrera", "email": "lucia@example.com", "plan": "Mensual" }
```
**Respuesta (201):**
```json
{ "_id": "6650f1a2c3d4e5f6a7b8c902", "nombre": "Lucía Herrera", "email": "lucia@example.com", "plan": "Mensual", "activo": true }
```
Si el email ya existe: `400` → `{ "error": "Ya existe un miembro con el email lucia@example.com" }`

### Actualizar miembro
**Método:** `PUT`
**URL:** `http://127.0.0.1:5000/api/v1/miembros/{id}`

**Body:**
```json
{ "plan": "VIP" }
```
**Respuesta (200):** el miembro con los cambios aplicados.

### Eliminar miembro
**Método:** `DELETE`
**URL:** `http://127.0.0.1:5000/api/v1/miembros/{id}`

**Respuesta (200):**
```json
{ "mensaje": "Miembro eliminado" }
```
Si el miembro tiene reservas: `409` → `{ "error": "No se puede eliminar: el miembro tiene reservas registradas" }`

---

## 🧘 Clases

| Campo | Tipo | Requerido (POST) | Descripción |
|-------|------|:---:|-------------|
| `nombre` | string | ✅ | Nombre de la clase |
| `entrenador_id` | ObjectId (string) | ✅ | Debe existir en `entrenadores` |
| `categoria` | string | ✅ | Ej. Cardio, Flexibilidad, Contacto |
| `cupo_maximo` | entero > 0 | ✅ | Capacidad total |
| `cupo_actual` | entero ≥ 0 | ❌ | Por defecto `0`; no puede superar `cupo_maximo` |

### Obtener todas las clases
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/clases`

**Respuesta (200):**
```json
[
  {
    "_id": "60d5ecb8b5c9c22b1c8e0301",
    "nombre": "CrossFit Matutino",
    "entrenador_id": "60d5ecb8b5c9c22b1c8e0101",
    "categoria": "Alta Intensidad",
    "cupo_maximo": 15,
    "cupo_actual": 9
  }
]
```

### Obtener clase por ID
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/clases/{id}`
**Ejemplo:** `http://127.0.0.1:5000/api/v1/clases/60d5ecb8b5c9c22b1c8e0301`

**Respuesta (200):** la clase solicitada. Si no existe: `404` → `{ "error": "Clase no encontrada" }`

### Insertar clase
**Método:** `POST`
**URL:** `http://127.0.0.1:5000/api/v1/clases`

**Body:**
```json
{
  "nombre": "HIIT Nocturno",
  "entrenador_id": "60d5ecb8b5c9c22b1c8e0101",
  "categoria": "Alta Intensidad",
  "cupo_maximo": 12
}
```
**Respuesta (201):**
```json
{
  "_id": "6650f1a2c3d4e5f6a7b8c903",
  "nombre": "HIIT Nocturno",
  "entrenador_id": "60d5ecb8b5c9c22b1c8e0101",
  "categoria": "Alta Intensidad",
  "cupo_maximo": 12,
  "cupo_actual": 0
}
```
Si el entrenador no existe: `400` → `{ "error": "No existe el entrenador con id ..." }`

### Actualizar clase
**Método:** `PUT`
**URL:** `http://127.0.0.1:5000/api/v1/clases/{id}`

**Body:**
```json
{ "cupo_actual": 5 }
```
**Respuesta (200):** la clase con los cambios aplicados.

### Eliminar clase
**Método:** `DELETE`
**URL:** `http://127.0.0.1:5000/api/v1/clases/{id}`

**Respuesta (200):**
```json
{ "mensaje": "Clase eliminada" }
```
Si la clase tiene reservas: `409` → `{ "error": "No se puede eliminar: la clase tiene reservas registradas" }`

---

## 🎟️ Reservas

| Campo | Tipo | Requerido (POST) | Descripción |
|-------|------|:---:|-------------|
| `miembro_id` | ObjectId (string) | ✅ | Debe existir en `miembros` |
| `fecha` | string ISO 8601 | ✅ | Ej. `2026-10-01T08:00:00Z` |
| `clases_reservadas` | arreglo | ✅ | Al menos un elemento `{ clase_id, pases, costo }` |
| `clases_reservadas[].clase_id` | ObjectId (string) | ✅ | Debe existir en `clases` |
| `clases_reservadas[].pases` | entero > 0 | ✅ | Cantidad de pases |
| `clases_reservadas[].costo` | número ≥ 0 | ✅ | Costo por pase |
| `estado_pago` | string | ❌ | Ej. `Confirmado` |

> `monto_total` **no se envía**: la API lo calcula como la suma de `pases × costo`.

### Obtener todas las reservas
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/reservas`

**Respuesta (200):**
```json
[
  {
    "_id": "60d5ecb8b5c9c22b1c8e0401",
    "miembro_id": "60d5ecb8b5c9c22b1c8e0201",
    "fecha": "2026-10-01T08:00:00Z",
    "clases_reservadas": [
      { "clase_id": "60d5ecb8b5c9c22b1c8e0301", "pases": 1, "costo": 10.0 },
      { "clase_id": "60d5ecb8b5c9c22b1c8e0303", "pases": 1, "costo": 12.0 }
    ],
    "monto_total": 22.0,
    "estado_pago": "Confirmado"
  }
]
```

### Obtener reserva por ID
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/reservas/{id}`
**Ejemplo:** `http://127.0.0.1:5000/api/v1/reservas/60d5ecb8b5c9c22b1c8e0401`

**Respuesta (200):** la reserva solicitada. Si no existe: `404` → `{ "error": "Reserva no encontrada" }`

### Insertar reserva
**Método:** `POST`
**URL:** `http://127.0.0.1:5000/api/v1/reservas`

**Body:**
```json
{
  "miembro_id": "60d5ecb8b5c9c22b1c8e0204",
  "fecha": "2026-10-05T07:00:00Z",
  "clases_reservadas": [
    { "clase_id": "60d5ecb8b5c9c22b1c8e0304", "pases": 2, "costo": 12.50 }
  ]
}
```
**Respuesta (201):**
```json
{
  "_id": "6650f1a2c3d4e5f6a7b8c904",
  "miembro_id": "60d5ecb8b5c9c22b1c8e0204",
  "fecha": "2026-10-05T07:00:00Z",
  "clases_reservadas": [
    { "clase_id": "60d5ecb8b5c9c22b1c8e0304", "pases": 2, "costo": 12.5 }
  ],
  "monto_total": 25.0
}
```

### Actualizar reserva
**Método:** `PUT`
**URL:** `http://127.0.0.1:5000/api/v1/reservas/{id}`

**Body:**
```json
{ "estado_pago": "Confirmado" }
```
**Respuesta (200):** la reserva con los cambios aplicados. Si se envía `clases_reservadas`, el `monto_total` se recalcula.

### Eliminar reserva
**Método:** `DELETE`
**URL:** `http://127.0.0.1:5000/api/v1/reservas/{id}`

**Respuesta (200):**
```json
{ "mensaje": "Reserva eliminada" }
```

---

## 📊 Reportes

Endpoints de solo lectura basados en las consultas de agregación de [database/script.mongodb.js](database/script.mongodb.js). Equivalencias con el enunciado:

| Enunciado | FitZone |
|-----------|---------|
| Marcas | Entrenadores |
| Prendas | Clases |
| Ventas | Reservas (pases vendidos) |
| Stock | Cupo restante (`cupo_maximo - cupo_actual`) |

### Entrenadores (marcas) con al menos una reserva (venta)
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/reportes/entrenadores-con-reservas`

**Respuesta (200):**
```json
[
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0102", "entrenador": "Ana Morales", "especialidad": "Yoga" },
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0101", "entrenador": "Carlos Ruiz", "especialidad": "CrossFit & High Intensity" },
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0103", "entrenador": "David Vega", "especialidad": "Spinning" },
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0105", "entrenador": "Esteban Solís", "especialidad": "Boxeo" },
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0106", "entrenador": "Mariana Rojas", "especialidad": "Zumba" }
]
```

### Clases (prendas) reservadas con su cupo (stock) restante
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/reportes/clases-cupo-restante`

**Respuesta (200):**
```json
[
  { "clase_id": "60d5ecb8b5c9c22b1c8e0305", "clase": "Boxeo Técnico", "pases_vendidos": 1, "cupo_maximo": 10, "cupo_actual": 6, "cupo_restante": 4 },
  { "clase_id": "60d5ecb8b5c9c22b1c8e0301", "clase": "CrossFit Matutino", "pases_vendidos": 4, "cupo_maximo": 15, "cupo_actual": 9, "cupo_restante": 6 },
  { "clase_id": "60d5ecb8b5c9c22b1c8e0302", "clase": "Power Yoga", "pases_vendidos": 2, "cupo_maximo": 20, "cupo_actual": 18, "cupo_restante": 2 },
  { "clase_id": "60d5ecb8b5c9c22b1c8e0303", "clase": "Spinning Extremo", "pases_vendidos": 1, "cupo_maximo": 25, "cupo_actual": 20, "cupo_restante": 5 },
  { "clase_id": "60d5ecb8b5c9c22b1c8e0306", "clase": "Zumba Fitness", "pases_vendidos": 1, "cupo_maximo": 30, "cupo_actual": 25, "cupo_restante": 5 }
]
```

### Top 5 entrenadores (marcas) con más pases vendidos
**Método:** `GET`
**URL:** `http://127.0.0.1:5000/api/v1/reportes/top-entrenadores`

**Respuesta (200):**
```json
[
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0101", "entrenador": "Carlos Ruiz", "total_pases_vendidos": 4 },
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0102", "entrenador": "Ana Morales", "total_pases_vendidos": 2 },
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0103", "entrenador": "David Vega", "total_pases_vendidos": 1 },
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0105", "entrenador": "Esteban Solís", "total_pases_vendidos": 1 },
  { "entrenador_id": "60d5ecb8b5c9c22b1c8e0106", "entrenador": "Mariana Rojas", "total_pases_vendidos": 1 }
]
```

---
👥 Integrantes del Proyecto

-Greivin González Trejos
-Joselyn Solano Monge
