const Usuario = require("../models/usuarioModel.js"); 
const jwt = require('jsonwebtoken');
const SECRET_KEY = process.env.JWT_SECRET || 'clave-secreta-supersegura';
async function getUsuario(req, res){
  try {
    const rows = await Usuario.getUsuario();
    if (!rows || rows.length === 0) {
      return res.status(404).json({ error: "No hay usuario registrado" });
    }
    res.json(rows[0]); 
  } catch (error) {
    console.error("Error al obtener el usuario:", error);
    res.status(500).json({ error: "Error interno del servidor" });
  }
}
async function loginUsuario(req, res) {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email y contraseña requeridos' });
    }

    const usuario = await Usuario.login({ email, password });
    if (!usuario) {
      return res.status(401).json({ error: 'Credenciales inválidas' });
    }

    const token = jwt.sign(
      { id: usuario.id},
      SECRET_KEY,
      { expiresIn: '2h' }
    );

    res.status(200).json({
      mensaje: 'Login exitoso',
      usuario: {
        email: usuario.email,
      },
      token
    });

  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function updateUsuario(req, res) {
  try {
    
    const {user_email, user_pass, monto_total} = req.body
    console.log(user_pass)
    const usuario = await Usuario.update(user_email, user_pass, monto_total);
    if (!usuario) return res.status(404).json({ error: "Usuario no encontrado" });
    res.json(usuario);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
} 


module.exports = {getUsuario, updateUsuario, loginUsuario};