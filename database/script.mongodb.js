
// 1. CREACIÓN Y SELECCIÓN DE BASE DE DATOS

use('fitzone_db')

// Limpieza previa de colecciones
db.miembros.drop();
db.entrenadores.drop();
db.clases.drop();
db.reservas.drop();



// 2. OPERACIONES CRUD POR COLECCIÓN


// --- COLECCIÓN 1: ENTRENADORES ---
// Insertar un dato
db.entrenadores.insertOne({
  _id: ObjectId("60d5ecb8b5c9c22b1c8e0101"),
  nombre: "Carlos Ruiz",
  especialidad: "CrossFit",
  activo: true
});

// Insertar varios datos
db.entrenadores.insertMany([
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0102"), nombre: "Ana Morales", especialidad: "Yoga", activo: true },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0103"), nombre: "David Vega", especialidad: "Spinning", activo: true },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0104"), nombre: "Laura Gómez", especialidad: "Pilates", activo: true },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0105"), nombre: "Esteban Solís", especialidad: "Boxeo", activo: true },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0106"), nombre: "Mariana Rojas", especialidad: "Zumba", activo: true }
]);

// Actualizar un dato
db.entrenadores.updateOne(
  { nombre: "Carlos Ruiz" },
  { $set: { especialidad: "CrossFit & High Intensity" } }
);

// Eliminar un dato
db.entrenadores.insertOne({ _id: ObjectId("60d5ecb8b5c9c22b1c8e0199"), nombre: "Prueba Temp", activo: false });
db.entrenadores.deleteOne({ _id: ObjectId("60d5ecb8b5c9c22b1c8e0199") });


// --- COLECCIÓN 2: MIEMBROS ---
// Insertar un dato
db.miembros.insertOne({
  _id: ObjectId("60d5ecb8b5c9c22b1c8e0201"),
  nombre: "Sonia Araya",
  email: "sonia@example.com",
  plan: "VIP",
  activo: true
});

// Insertar varios datos
db.miembros.insertMany([
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0202"), nombre: "Roberto Méndez", email: "roberto@example.com", plan: "Mensual", activo: true },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0203"), nombre: "Valeria Castro", email: "valeria@example.com", plan: "VIP", activo: true },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0204"), nombre: "Gabriel Vargas", email: "gabriel@example.com", plan: "Básico", activo: true }
]);

// Actualizar un dato
db.miembros.updateOne(
  { email: "roberto@example.com" },
  { $set: { plan: "VIP" } }
);

// Eliminar un dato
db.miembros.insertOne({ _id: ObjectId("60d5ecb8b5c9c22b1c8e0299"), nombre: "Miembro Test", email: "test@example.com" });
db.miembros.deleteOne({ _id: ObjectId("60d5ecb8b5c9c22b1c8e0299") });


// --- COLECCIÓN 3: CLASES ---
// Insertar un dato
db.clases.insertOne({
  _id: ObjectId("60d5ecb8b5c9c22b1c8e0301"),
  nombre: "CrossFit Matutino",
  entrenador_id: ObjectId("60d5ecb8b5c9c22b1c8e0101"), // Carlos Ruiz
  categoria: "Alta Intensidad",
  cupo_maximo: 15,
  cupo_actual: 10
});

// Insertar varios datos
db.clases.insertMany([
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0302"), nombre: "Power Yoga", entrenador_id: ObjectId("60d5ecb8b5c9c22b1c8e0102"), categoria: "Flexibilidad", cupo_maximo: 20, cupo_actual: 18 },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0303"), nombre: "Spinning Extremo", entrenador_id: ObjectId("60d5ecb8b5c9c22b1c8e0103"), categoria: "Cardio", cupo_maximo: 25, cupo_actual: 20 },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0304"), nombre: "Pilates Core", entrenador_id: ObjectId("60d5ecb8b5c9c22b1c8e0104"), categoria: "Flexibilidad", cupo_maximo: 12, cupo_actual: 8 },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0305"), nombre: "Boxeo Técnico", entrenador_id: ObjectId("60d5ecb8b5c9c22b1c8e0105"), categoria: "Contacto", cupo_maximo: 10, cupo_actual: 6 },
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0306"), nombre: "Zumba Fitness", entrenador_id: ObjectId("60d5ecb8b5c9c22b1c8e0106"), categoria: "Cardio", cupo_maximo: 30, cupo_actual: 25 }
]);

// Actualizar un dato
db.clases.updateOne(
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0301") },
  { $inc: { cupo_actual: -1 } }
);

// Eliminar un dato
db.clases.insertOne({ _id: ObjectId("60d5ecb8b5c9c22b1c8e0399"), nombre: "Clase Cancelada", cupo_maximo: 0 });
db.clases.deleteOne({ _id: ObjectId("60d5ecb8b5c9c22b1c8e0399") });


// --- COLECCIÓN 4: RESERVAS ---
// Insertar un dato
db.reservas.insertOne({
  _id: ObjectId("60d5ecb8b5c9c22b1c8e0401"),
  miembro_id: ObjectId("60d5ecb8b5c9c22b1c8e0201"),
  fecha: ISODate("2026-10-01T08:00:00Z"),
  clases_reservadas: [
    { clase_id: ObjectId("60d5ecb8b5c9c22b1c8e0301"), pases: 1, costo: 10.00 },
    { clase_id: ObjectId("60d5ecb8b5c9c22b1c8e0303"), pases: 1, costo: 12.00 }
  ],
  monto_total: 22.00
});

// Insertar varios datos
db.reservas.insertMany([
  {
    _id: ObjectId("60d5ecb8b5c9c22b1c8e0402"),
    miembro_id: ObjectId("60d5ecb8b5c9c22b1c8e0202"),
    fecha: ISODate("2026-10-01T10:30:00Z"),
    clases_reservadas: [
      { clase_id: ObjectId("60d5ecb8b5c9c22b1c8e0302"), pases: 2, costo: 15.00 },
      { clase_id: ObjectId("60d5ecb8b5c9c22b1c8e0306"), pases: 1, costo: 10.00 }
    ],
    monto_total: 40.00
  },
  {
    _id: ObjectId("60d5ecb8b5c9c22b1c8e0403"),
    miembro_id: ObjectId("60d5ecb8b5c9c22b1c8e0203"),
    fecha: ISODate("2026-10-02T09:00:00Z"),
    clases_reservadas: [
      { clase_id: ObjectId("60d5ecb8b5c9c22b1c8e0301"), pases: 3, costo: 10.00 },
      { clase_id: ObjectId("60d5ecb8b5c9c22b1c8e0305"), pases: 1, costo: 15.00 }
    ],
    monto_total: 45.00
  }
]);

// Actualizar un dato
db.reservas.updateOne(
  { _id: ObjectId("60d5ecb8b5c9c22b1c8e0401") },
  { $set: { estado_pago: "Confirmado" } }
);

// Eliminar un dato
db.reservas.insertOne({ _id: ObjectId("60d5ecb8b5c9c22b1c8e0499"), monto_total: 0 });
db.reservas.deleteOne({ _id: ObjectId("60d5ecb8b5c9c22b1c8e0499") });


// 3. CONSULTAS REQUERIDAS 


// i. Consulta: Obtener la cantidad vendida/reservada de pases a clases por fecha y filtrarla con una fecha específica.
// Explicación: Filtra las reservas efectuadas el día '2026-10-01', desglosa el arreglo de pases ($unwind) y agrupa calculando la suma total de pases vendidos para ese día.
db.reservas.aggregate([
  {
    $match: {
      fecha: {
        $gte: ISODate("2026-10-01T00:00:00Z"),
        $lt: ISODate("2026-10-02T00:00:00Z")
      }
    }
  },
  { $unwind: "$clases_reservadas" },
  {
    $group: {
      _id: { $dateToString: { format: "%Y-%m-%d", date: "$fecha" } },
      total_pases_reservados: { $sum: "$clases_reservadas.pases" }
    }
  }
]);


// ii. Consulta: Obtener la lista de todos los entrenadores que tienen al menos una reserva/venta registrada.
// Explicación: Desglosa los pases reservados, relaciona ($lookup) la clase correspondiente para obtener el ID del entrenador, vuelve a enlazar ($lookup) con la colección de entrenadores y agrupa descartando duplicados.
db.reservas.aggregate([
  { $unwind: "$clases_reservadas" },
  {
    $lookup: {
      from: "clases",
      localField: "clases_reservadas.clase_id",
      foreignField: "_id",
      as: "clase_info"
    }
  },
  { $unwind: "$clase_info" },
  {
    $lookup: {
      from: "entrenadores",
      localField: "clase_info.entrenador_id",
      foreignField: "_id",
      as: "entrenador_info"
    }
  },
  { $unwind: "$entrenador_info" },
  {
    $group: {
      _id: "$entrenador_info._id",
      entrenador: { $first: "$entrenador_info.nombre" },
      especialidad: { $first: "$entrenador_info.especialidad" }
    }
  },
  { $project: { _id: 0, entrenador: 1, especialidad: 1 } }
]);


// iii. Consulta: Obtener clases reservadas y su cantidad restante en cupo/stock.
// Explicación: Suma la cantidad de pases comercializados por cada clase y cruza ($lookup) con la colección 'clases' para proyectar el nombre del curso y calcular la diferencia disponible respecto al cupo máximo.
db.reservas.aggregate([
  { $unwind: "$clases_reservadas" },
  {
    $group: {
      _id: "$clases_reservadas.clase_id",
      total_pases_vendidos: { $sum: "$clases_reservadas.pases" }
    }
  },
  {
    $lookup: {
      from: "clases",
      localField: "_id",
      foreignField: "_id",
      as: "clase_info"
    }
  },
  { $unwind: "$clase_info" },
  {
    $project: {
      _id: 0,
      clase: "$clase_info.nombre",
      reservas_realizadas: "$total_pases_vendidos",
      cupo_restante: { $subtract: ["$clase_info.cupo_maximo", "$clase_info.cupo_actual"] }
    }
  }
]);


// iv. Consulta: Obtener listado de los 5 entrenadores con más pases/ventas y su cantidad.
// Explicación: Une cada reserva con su clase y entrenador correspondiente. Suma el total de pases acumulados por entrenador, ordena de forma descendente ($sort) y proyecta únicamente el Top 5 ($limit).
db.reservas.aggregate([
  { $unwind: "$clases_reservadas" },
  {
    $lookup: {
      from: "clases",
      localField: "clases_reservadas.clase_id",
      foreignField: "_id",
      as: "clase_info"
    }
  },
  { $unwind: "$clase_info" },
  {
    $lookup: {
      from: "entrenadores",
      localField: "clase_info.entrenador_id",
      foreignField: "_id",
      as: "entrenador_info"
    }
  },
  { $unwind: "$entrenador_info" },
  {
    $group: {
      _id: "$entrenador_info.nombre",
      total_reservas: { $sum: "$clases_reservadas.pases" }
    }
  },
  { $sort: { total_reservas: -1 } },
  { $limit: 5 },
  {
    $project: {
      _id: 0,
      entrenador: "$_id",
      total_reservas: 1
    }
  }
]);