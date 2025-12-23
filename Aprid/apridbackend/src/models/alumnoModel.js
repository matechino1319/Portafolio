const db = require("../config/db"); 

class Alumno {
  static async create({ dni, nombre, apellido, contacto, tutor, espacio_curricular}) {
    
    const [result] = await db.query(
      "INSERT INTO alumnos (dni, nombre, apellido, contacto, tutor, espacio_curricular) VALUES (?, ?, ?, ?, ?, ?)",
      [dni, nombre, apellido, contacto, tutor, espacio_curricular]
    );
    return { dni, nombre, apellido, contacto, tutor, espacio_curricular };
  }

  static async getAll() {
    const [rows] = await db.query("SELECT * FROM alumnos");
    return rows;
  }

  static async getByDni(dni) {
    const [rows] = await db.query("SELECT * FROM alumnos WHERE dni = ?", [dni]);
    return rows[0];
  }

  static async update(dni, { nombre, apellido, contacto, tutor, espacio_curricular }) {
    const [result] = await db.query(
      "UPDATE alumnos SET nombre = ?, apellido = ?, contacto = ?, tutor = ?, espacio_curricular = ? WHERE dni = ?",
      [nombre, apellido, contacto, tutor, espacio_curricular, dni]
    );
    return result.affectedRows > 0 ? { dni, nombre, apellido, contacto, tutor, espacio_curricular } : null;
  }

  static async delete(dni) {
    const [result] = await db.query("DELETE FROM alumnos WHERE dni = ?", [dni]);
    return result.affectedRows > 0;
  }
}

module.exports = Alumno;
