import "../styles/ajustes.css";
import { useAjustes } from "../context/AjustesContext.jsx";
import Header from "../components/Header.jsx";
import { useState } from "react";
import CuentaModal from "../components/CuentaModal.jsx";

function Ajustes() {
  const { ajustes, setAjustes } = useAjustes();
  const [editando, setEditando] = useState(null);

  const handleEditar = async () => {
    try {
      const res = await fetch("http://localhost:3000/usuario"); 
      if (!res.ok) throw new Error("No se pudo obtener el usuario");
      const usuario = await res.json();
      setEditando(usuario); // pasamos los datos al modal
    } catch (err) {
      console.error(err);
      alert("No se pudo cargar la información del usuario");
    }
  };
  const actualizarUsuario = (usuarioActualizado) => {
    setEditando(null); // cierra el modal
    console.log("Usuario actualizado:", usuarioActualizado);
  };

  const handleColorChange = (e, key) => {
    setAjustes({
      ...ajustes,
      colores: { ...ajustes.colores, [key]: e.target.value },
    });
  };

  const handleTamanoChange = (e) => {
    setAjustes({ ...ajustes, tamano: parseInt(e.target.value) });
  };

  const handleTemaChange = (nuevoTema) => {
    setAjustes({ ...ajustes, tema: nuevoTema });
  };

  return (
    <>
      <Header />

      <main
        className="general-container"
        style={{ fontSize: `${ajustes.tamano}px` }}
      >
          <h1>Ajustes</h1>
        <section className="ajustes-card">

          <div className="bloque">
            <h3>Modificar datos:</h3>
            <div className="opciones">
               <button onClick={handleEditar}>Editar configuracion de la cuenta</button>
            </div>
          </div>

          <div className="bloque">
            <h3>Apariencia:</h3>

            <div className="tema">
              <p>Tema:</p>
              <button
                className={`btn-tema ${ajustes.tema === "claro" ? "activo" : ""}`}
                onClick={() => handleTemaChange("claro")}
              >
                Claro
              </button>
              <button
                className={`btn-tema oscuro ${ajustes.tema === "oscuro" ? "activo" : ""}`}
                onClick={() => handleTemaChange("oscuro")}
              >
                Oscuro
              </button>
            </div>

            <div className="fuente">
              <label htmlFor="tamano">Tamaño de fuente:</label>
              <input
                type="range"
                id="tamano"
                min="12"
                max="24"
                value={ajustes.tamano}
                onChange={handleTamanoChange}
              />
              <span>{ajustes.tamano}px</span>
            </div>
          </div>

          <div className="bloque">
            <h3>Cambiar color:</h3>
            <div className="colores">
              <div className="item">
                <p>Barra lateral:</p>
                <input type="color" value={ajustes.colores.barraLateral} onChange={(e) => handleColorChange(e, "barraLateral")} />
              </div>
              <div className="item">
                <p>Botones:</p>
                <input type="color" value={ajustes.colores.botones} onChange={(e) => handleColorChange(e, "botones")} />
              </div>
              <div className="item">
                <p>Letra:</p>
                <input type="color" value={ajustes.colores.letra} onChange={(e) => handleColorChange(e, "letra")} />
              </div>
              <div className="item">
                <p>Logo:</p>
                <input type="color" value={ajustes.colores.logo} onChange={(e) => handleColorChange(e, "logo")} />
                <div className="cuadro" style={{ backgroundColor: ajustes.colores.logo }}></div>
              </div>
            </div>
          </div>
        </section>
      </main>
      {editando && (
        <CuentaModal
          usuario={editando}
          onClose={() => setEditando(null)}
          onSave={actualizarUsuario}
        />
)}
    </>
  );
}

export default Ajustes;
