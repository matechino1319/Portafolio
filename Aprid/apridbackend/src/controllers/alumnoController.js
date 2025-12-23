const Alumno = require("../models/alumnoModel.js"); 

async function createAlumno(req, res) {
  try {
    const alumno = await Alumno.create(req.body);
    res.status(201).json(alumno);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function getAlumnos(req, res) {
  try {
    const alumnos = await Alumno.getAll();
    res.json(alumnos);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function getAlumnoById(req, res) {
  try {
    const alumno = await Alumno.getByDni(req.params.id);
    if (!alumno) return res.status(404).json({ error: "Alumno no encontrado" });
    res.json(alumno);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function updateAlumno(req, res) {
  try {
    const alumno = await Alumno.update(req.params.id, req.body);
    if (!alumno) return res.status(404).json({ error: "Alumno no encontrado" });
    res.json(alumno);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

async function deleteAlumno(req, res) {
  try {
    console.log(req.params.id)
    const deleted = await Alumno.delete(req.params.id);
    if (!deleted) return res.status(404).json({ error: "Alumno no encontrado" });
    res.json({ message: "Alumno eliminado" });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}

module.exports = { createAlumno, getAlumnos, getAlumnoById, updateAlumno, deleteAlumno };
