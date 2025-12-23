const db = require("../config/db");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

const SECRET_KEY = process.env.JWT_SECRET || "xlmq9990xlskskhfeie1923h3n3r87r";

class Usuario {
  static async getUsuario() {
    const [rows] = await db.query("SELECT * FROM usuarios LIMIT 1");
    return rows;
  }

  static async login({ user_email, user_pass }) {
    try {
      const [rows] = await db.query("SELECT * FROM usuarios WHERE user_email = ?", [user_email]);
      if (rows.length === 0) return null;

      const user = rows[0];
      //const validPassword = await bcrypt.compare(user_pass, user.user_pass);
      const validPassword = user_pass === user.user_pass;
      console.log(user)
      console.log(validPassword)
      if (!validPassword) return null;

      const token = jwt.sign({ id: user.id }, SECRET_KEY, { expiresIn: "2h" });

      return {
        id: user.id,
        email: user.user_email,
        token,
      };
    } catch (error) {
      console.error("Error en login:", error);
      throw error;
    }
  }

  static async update(email,  password, monto_total ) {
  try {
    if (!email) throw new Error("Email requerido para actualizar usuario");
    console.log(email, password, monto_total)
    const sql = 
      `UPDATE usuarios 
      SET user_email = ?, user_pass = ?, monto_total = ?
      WHERE id = 1
    ;`

    const valores = [email, password, monto_total];

    const [result] = await db.query(sql, valores);

    if (result.affectedRows === 0) return null;

    return { message: "Usuario actualizado con éxito" };
  } catch (error) {
    console.error("Error en update:", error);
    throw error;
  }
}}
module.exports = Usuario;
