const express = require('express');
const jwt = require('jsonwebtoken');
const router = express.Router();
const Usuario = require('../models/usuarioModel.js');  // Asegurate que el path sea correcto

const SECRET_KEY = "8d7f2b1e5a3c9a6d0f4g2h8i1j7k3l5m9n"; 

// 🟢 LOGIN DESDE BASE DE DATOS
router.post('/login', async (req, res) => {
  try {
    const { usuario, password } = req.body;
    console.log(usuario, password)
    // Validar que vengan los datos
    if (!usuario || !password) {
      return res.status(400).json({ error: 'Email y contraseña requeridos' });
    }

    // Llamar al método del modelo
    const result = await Usuario.login({ user_email: usuario, user_pass: password });
    console.log(result)
    // Si hubo error, devolver mensaje
    if (result.error) {
      return res.status(401).json({ error: result.error });
    }

    res.status(200).json({
      message: "Inicio de sesión exitoso",
      token: result.token,
      user: result.email,
    });
  } catch (error) {
    console.error("Error en /login:", error);
    res.status(500).json({ error: "Error interno del servidor" });
  }
});

module.exports = router;
