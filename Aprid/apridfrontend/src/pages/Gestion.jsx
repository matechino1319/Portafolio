import "../styles/gestion.css";
import { Link } from "react-router-dom";
import { useAjustes } from "../context/AjustesContext.jsx";
import Header from "../components/Header.jsx";
import { useState, useEffect } from "react";

function Gestion() {
  const { ajustes } = useAjustes();
  const [alumnos, setAlumnos] = useState([]);
  const [busqueda, setBusqueda] = useState("");

  useEffect(() => {
    const fetchAlumnos = async () => {
      try {
        const res = await fetch("http://localhost:3000/alumnos");
        if (!res.ok) throw new Error("Error al cargar los alumnos");
        const data = await res.json();
        setAlumnos(data);
      } catch (err) {
        console.error("Error al cargar alumnos:", err);
        alert("Ocurrió un error al cargar los alumnos");
      }
    };

    fetchAlumnos();
  }, []);

  const filtrados = alumnos.filter((alumno) => {
    const texto = busqueda.toLowerCase();
    return (
      alumno.nombre.toLowerCase().includes(texto) ||
      alumno.apellido.toLowerCase().includes(texto) ||
      alumno.dni.toString().includes(texto)
    );
  });

  return (
    <>
      <Header />

      <main
        className="general-container"
        style={{
          fontSize: `${ajustes.tamano}px`,
          color: ajustes.colores.letra,
        }}
      >
        <div className="gestion-header">
          <h1>Gestión de alumnos</h1>

          <Link
            to="/agregar"
            className="btn-add"
            style={{
              backgroundColor: ajustes.colores.botones,
              color: ajustes.colores.letra,
            }}
          >
            Añadir alumno
          </Link>
        </div>

        <div className="buscar-wrapper">
          <input
            type="text"
            placeholder="Buscar por nombre o DNI..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
        </div>

        <div className="tabla-wrapper">
          <table>
            <thead>
              <tr>
                <th>Alumno</th>
                <th>D.N.I</th>
                <th>Tutor</th>
                <th>Teléfono</th>
                <th>Editar</th>
              </tr>
            </thead>
            <tbody>
              {filtrados.length > 0 ? (
                filtrados.map((r) => (
                  <tr key={r.dni}>
                    <td>{r.nombre} {r.apellido}</td>
                    <td>{r.dni}</td>
                    <td>{r.tutor}</td>
                    <td>{r.contacto}</td>
                    <td>
                      <Link to={`/editar/${r.dni}`}>✏️</Link>
                      <Link to={`/informe?dni=${r.dni}`}>📊</Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="mensaje-vacio">
                    No hay alumnos cargados todavía
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </main>

    </>
  );
}

export default Gestion;
