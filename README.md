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

 🏋️ Entrenadores
```json
{
  "_id": "60d5ecb8b5c9c22b1c8e0101",
  "nombre": "Carlos Ruiz",
  "especialidad": "CrossFit",
  "activo": true
}

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
    }
  ],
  "monto_total": 22.00
}

👥 Integrantes del Proyecto
```json
Greivin González Trejos

Joselyn Solano Monge

