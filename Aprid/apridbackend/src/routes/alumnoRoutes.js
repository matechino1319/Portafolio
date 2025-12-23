const express = require('express');
const router = express.Router();
const ctrl = require('../controllers/alumnoController');

router.post('/', ctrl.createAlumno);
router.get('/', ctrl.getAlumnos);
router.get('/:id', ctrl.getAlumnoById);
router.put('/:id', ctrl.updateAlumno);
router.delete('/:id', ctrl.deleteAlumno);

module.exports = router;
