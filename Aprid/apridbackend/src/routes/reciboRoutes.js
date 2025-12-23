const express = require('express');
const router = express.Router();
const ctrl = require('../controllers/reciboController');

router.post('/', ctrl.createRecibo);
router.get('/', ctrl.getRecibos);
router.get('/:id', ctrl.getReciboById);
router.put('/:id', ctrl.updateRecibo);
router.delete('/:id', ctrl.deleteRecibo);

module.exports = router;
