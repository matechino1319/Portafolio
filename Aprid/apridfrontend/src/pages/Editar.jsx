import "../styles/editar.css";
import { Link, useParams, useNavigate } from "react-router-dom";
import { useAjustes } from "../context/AjustesContext.jsx";
import { useEffect, useState } from "react";
import Header from "../components/Header.jsx";

function Editar() {
    const navigate = useNavigate();
    const { dni } = useParams();
    const { ajustes } = useAjustes();

    const [formData, setFormData] = useState({
        dni: "",
        nombre: "",
        apellido: "",
        tutor: "",
        contacto: "",
        espacio_curricular: "",
    });
    useEffect(() => {
        const fetchAlumno = async () => {
            try {
                const res = await fetch(`http://localhost:3000/alumnos/${dni}`);
                const data = await res.json();
                setFormData(data);
            } catch (error) {
                console.error("Error al cargar alumno:", error);
            }
        };
        fetchAlumno();
    }, [dni]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };
    const handleSubmitAlumno = async (e) => {
        e.preventDefault();

        try {
            const res = await fetch(`http://localhost:3000/alumnos/${dni}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (!res.ok) throw new Error("Error al actualizar el alumno");

            alert("Alumno actualizado correctamente");
            navigate("/gestion");
        } catch (error) {
            console.error(error);
            alert("Ocurrió un error al actualizar el alumno");
        }
    };
    const handleDelete = async (dni) => {
        if (!window.confirm("¿Estás seguro de que querés eliminar este alumno?")) return;

        try {
            const res = await fetch(`http://localhost:3000/alumnos/${dni}`, {
                method: "DELETE",
            });

            if (!res.ok) throw new Error("Error al eliminar el alumno");

            alert("Alumno eliminado correctamente");
            navigate("/gestion");
        } catch (error) {
            console.error(error);
            alert("Ocurrió un error al eliminar el alumno");
        }
    };
    return (
        <>
            <Header />
            <main className="general-container" style={{ fontSize: `${ajustes.tamano}px` }}>
                <div className="editar-content">
                    <form onSubmit={handleSubmitAlumno} className="editar-form">
                        <div className="form-row">
                            <h2>Datos del Alumno</h2>
                            <div className="form-row">
                                <label htmlFor="dni">DNI:</label>
                                <input type="number" id="dni" name="dni" value={formData.dni} onChange={handleChange} required />
                            </div>

                            <div className="form-grid">
                                <div className="form-row">
                                    <label htmlFor="nombre">Nombre:</label>
                                    <input type="text" id="nombre" name="nombre" value={formData.nombre} onChange={handleChange} required />
                                </div>

                                <div className="form-row">
                                    <label htmlFor="apellido">Apellido:</label>
                                    <input type="text" id="apellido" name="apellido" value={formData.apellido} onChange={handleChange} required />
                                </div>
                            </div>

                            <h2>Datos del Tutor</h2>

                            <div className="form-grid">
                                <div className="form-row">
                                    <label htmlFor="tutor">Nombre y Apellido:</label>
                                    <input type="text" id="tutor" name="tutor" value={formData.tutor} onChange={handleChange} required />
                                </div>

                                <div className="form-row">
                                    <label htmlFor="contacto">Número de teléfono:</label>
                                    <input type="tel" id="contacto" name="contacto" value={formData.contacto} onChange={handleChange} required />
                                </div>
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
                            Guardar cambios
                        </button>

                    </form>
                    <button onClick={() => handleDelete(formData.dni)} className="btn-delete">
                        Eliminar
                    </button>
                    </div>

            </main>
        </>
    )
}
export default Editar;