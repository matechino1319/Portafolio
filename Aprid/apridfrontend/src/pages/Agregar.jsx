import "../styles/editar.css";
import { useState } from "react";
import { useAjustes } from "../context/AjustesContext.jsx";
import Header from "../components/Header.jsx";

function Agregar() {
  const { ajustes } = useAjustes();
  const [formData, setFormData] = useState({
    dni: "",
    nombre: "",
    apellido: "",
    tutor: "",
    contacto: "",
    espacio_curricular: "",
  });

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmitAlumno = async (e) => {
    e.preventDefault();
    console.log(formData);

    try {
      const res = await fetch("http://localhost:3000/alumnos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData)
      });

      if (!res.ok) throw new Error("Error al registrar el alumno");

      const data = await res.json();
      console.log("Alumno registrado:", data);
      alert("Alumno registrado correctamente");

      // limpiar formulario
      setFormData({
        dni: "",
        nombre: "",
        apellido: "",
        tutor: "",
        contacto: "",
        espacio_curricular: "",
      });
    } catch (error) {
      console.error(error);
      alert("Ocurrió un error al registrar el alumno");
    }
  };
  return (
    <>
    <Header />
     <main className="general-container" style={{ fontSize: `${ajustes.tamano}px`, color: ajustes.colores.letra }}>
  <div className="editar-content">
    <form onSubmit={handleSubmitAlumno} className="editar-form">

      <h1>Agregar Alumno</h1>

      <h2>Datos del Alumno</h2>
      <div className="form-grid">
        <div className="form-row">
          <label htmlFor="dni">DNI:</label>
          <input type="number" id="dni" value={formData.dni} onChange={handleChange} placeholder="39438262" required />
        </div>

        <div className="form-row">
          <label htmlFor="espacio_curricular">Espacio curricular:</label>
          <input type="text" id="espacio_curricular" value={formData.espacio_curricular} onChange={handleChange} placeholder="Gastronomía" required />
        </div>

        <div className="form-row">
          <label htmlFor="nombre">Nombre:</label>
          <input type="text" id="nombre" value={formData.nombre} onChange={handleChange} placeholder="Pablo" required />
        </div>

        <div className="form-row">
          <label htmlFor="apellido">Apellido:</label>
          <input type="text" id="apellido" value={formData.apellido} onChange={handleChange} placeholder="Silva" required />
        </div>
      </div>

      <h2>Datos del Tutor</h2>
      <div className="form-grid">
        <div className="form-row">
          <label htmlFor="tutor">Nombre y Apellido:</label>
          <input type="text" id="tutor" value={formData.tutor} onChange={handleChange} placeholder="Pedro Silva" required />
        </div>

        <div className="form-row">
          <label htmlFor="contacto">Número de teléfono:</label>
          <input type="tel" id="contacto" value={formData.contacto} onChange={handleChange} placeholder="260468670" required />
        </div>
      </div>

      <button
        type="submit"
        className="btn"
        style={{
          backgroundColor: ajustes.colores.botones,
          color: ajustes.colores.letra,
        }}
      >
        Añadir Alumno ➜
      </button>
    </form>
  </div>
</main>

    </>
  );
}

export default Agregar;

