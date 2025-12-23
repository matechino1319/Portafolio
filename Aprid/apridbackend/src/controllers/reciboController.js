const Recibo = require("../models/reciboModel.js");
const Alumno = require("../models/alumnoModel.js");
const wpp = require("../controllers/whatsappController.js");

async function createRecibo(req, res) {
  try {
    console.log(req.body);

    const recibo = await Recibo.create(req.body);

    const alumno = await Alumno.getByDni(recibo.dni_alumno);
    if (!alumno) {
      return res.status(404).json({ error: "Alumno no encontrado" });
    }

     await wpp.sendReceiptController({
      number: `549${alumno.contacto}`,
      message: `Se creó un nuevo recibo #${recibo.id_comprobante} para ${alumno.nombre}`,
      name: alumno.nombre,
      id_comprobante: recibo.id_comprobante,
      dni_alumno:alumno.dni,
      amount: recibo.monto_pagado,
      description: recibo.descripcion || "Pago de cuotas",
      cuantity: 1,
      fecha_pago: recibo.fecha_pago,
    });

    res.status(201).json(recibo);
  } catch (err) {
    console.log(err.message);
    res.status(500).json({ error: err.message });
  }
}


async function getRecibos(req, res) {
  try {
    const recibos = await Recibo.getAll();
    res.json(recibos);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function getReciboById(req, res) {
  try {
    const recibo = await Recibo.getById(req.params.id);
    if (!recibo) return res.status(404).json({ error: "Recibo no encontrado" });
    res.json(recibo);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function updateRecibo(req, res) {
  try {
    const data = { id_comprobante: req.params.id, ...req.body };
    const recibo = await Recibo.update(data);
    if (!recibo) return res.status(404).json({ error: "Recibo no encontrado" });
    res.json(recibo);
  } catch (err) {
    console.log(err.message);
    res.status(500).json({ error: err.message });
  }
}


async function deleteRecibo(req, res) {
  try {
    
    const deleted = await Recibo.delete(req.params.id);
    if (!deleted) return res.status(404).json({ error: "Recibo no encontrado" });
    console.log("Recibo eliminado");
    res.json({ message: "Recibo eliminado" });
  } catch (err) {
    console.log(err.message);
    res.status(500).json({ error: err.message });
  }
}

module.exports = { createRecibo, getRecibos, getReciboById, updateRecibo, deleteRecibo };