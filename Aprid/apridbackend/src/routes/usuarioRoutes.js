const express = require('express');
const router = express.Router();
const ctrl = require('../controllers/usuarioController');

router.get("/", ctrl.getUsuario);
router.post('/', ctrl.loginUsuario);
router.put('/', ctrl.updateUsuario);

module.exports = router;