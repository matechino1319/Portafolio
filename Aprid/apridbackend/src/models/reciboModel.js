const db = require("../config/db");

class Recibo {
static async create({ dni_alumno, monto_pagado, monto_total, fecha_pago, descripcion }) {
  try {
    const [alumno] = await db.query(
      "SELECT dni FROM alumnos WHERE dni = ?",
      [dni_alumno]
    );

    if (alumno.length === 0) {
      throw new Error(`El alumno con DNI ${dni_alumno} no existe`);
    }
    const [result] = await db.query(
      "INSERT INTO comprobantes_de_pago (dni_alumno, monto_pagado, monto_total, fecha_pago, descripcion) VALUES (?, ?, ?, ?, ?)",
      [dni_alumno, monto_pagado, monto_total, fecha_pago, descripcion]
    );

    if (result.affectedRows === 0) {
      throw new Error("No se pudo insertar el recibo");
    }

    return {
      id_comprobante: result.insertId,
      dni_alumno,
      monto_pagado,
      monto_total,
      fecha_pago,
      descripcion,
    };
  } catch (error) {
    console.error("Error al crear el recibo:", error);
    throw new Error("Error al crear el recibo: " + error.message);
  }
}


 static async getAll() {
  try {
    const [rows] = await db.query(`
      SELECT 
        c.id_comprobante,
        c.dni_alumno,
        a.nombre,
        a.apellido,
        c.fecha_pago,
        c.monto_total,
        c.monto_pagado,
        c.descripcion
      FROM comprobantes_de_pago c
      JOIN alumnos a ON c.dni_alumno = a.dni
      ORDER BY c.fecha_pago DESC
    `);
    return rows;
  } catch (error) {
    console.error("Error al obtener comprobantes:", error);
    throw new Error("Error al obtener comprobantes: " + error.message);
  }
}


  static async getById(id_comprobante) {
    const [rows] = await db.query("SELECT * FROM comprobantes_de_pago WHERE id_comprobante = ?", [id_comprobante]);
    return rows[0];
  }

  static async update({id_comprobante,dni_alumno, monto_pagado, fecha_pago, descripcion }) {
    console.log("checking");
    
    const [result] = await db.query(
      "UPDATE comprobantes_de_pago SET dni_alumno = ?, monto_pagado = ?, fecha_pago = ?, descripcion = ? WHERE id_comprobante = ?",
      [dni_alumno, monto_pagado, fecha_pago, descripcion, id_comprobante]
    );
    return result.affectedRows > 0 ? { id_comprobante, dni_alumno, monto_pagado, fecha_pago, descripcion } : null;
  }

  static async delete(id_comprobante) {
    
    const [result] = await db.query("DELETE FROM comprobantes_de_pago WHERE id_comprobante = ?", [id_comprobante]);
    return result.affectedRows > 0;
  }
}

module.exports = Recibo;