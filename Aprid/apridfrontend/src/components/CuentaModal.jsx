import "../styles/modal.css";
import { useState, useEffect } from "react";
import { useAjustes } from "../context/AjustesContext.jsx";

function CuentaModal({ usuario, onClose, onSave }) {
  const { ajustes, setAjustes } = useAjustes();
  const [formData, setFormData] = useState({
    user_email: usuario?.email || "",
    user_pass: usuario?.password || "",
    monto_total: usuario?.monto_total || 0,
  });

  useEffect(() => {
    const fetchUsuario = async () => {
      try {
        const res = await fetch("http://localhost:3000/usuario");
        if (!res.ok) throw new Error("No se pudo obtener el usuario");
        const usuario = await res.json();
        setFormData({
          user_email: usuario.user_email || "",
          user_pass: usuario.user_pass,
          monto_total: usuario.monto_total || 0,
        });
      } catch (err) {
        console.error("Error al cargar usuario:", err);
        alert("No se pudo cargar la información del usuario");
      }
    };

    fetchUsuario();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:3000/usuario", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error("Error al actualizar");
      const actualizado = await res.json();
      onSave(actualizado);
      setAjustes(prev => ({
        ...prev,
        monto: formData.monto_total
      }));
    } catch (err) {
      console.error(err);
      alert("No se pudo editar el usuario");
    }
  };

  return (
    <div className="modal-overlay">
      <form
        className="modal"
        onSubmit={handleSubmit}
        style={{
          fontSize: `${ajustes.tamano}px`,
          color: ajustes.colores.letra,
          backgroundColor: ajustes.tema === "oscuro" ? "#222" : "#fff",

        }}
      >
        <h2 style={{ color: ajustes.colores.logo }}>Editar cuenta</h2>

        <label>Correo:</label>
        <input
          type="text"
          value={formData.user_email}
          onChange={(e) => setFormData({ ...formData, user_email: e.target.value })}
          required
        />

        <label>Contrasenia:</label>
        <input
          type="text"
          value={formData.user_pass}
          onChange={(e) => setFormData({ ...formData, user_pass: e.target.value })}
          required
        />

        <label>Monto predeterminado:</label>
        <input
          type="number"
          value={formData.monto_total}
          onChange={(e) => setFormData({ ...formData, monto_total: e.target.value })}
          required
        />


        <div className="acciones">
          <button
            type="submit"
            className="btn-guardar"
            style={{ background: ajustes.colores.botones }}
          >
            Guardar cambios
          </button>
          <button
            type="button"
            onClick={onClose}
            className="btn-cancelar"
            style={{ background: ajustes.colores.logo }}
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}

export default CuentaModal;
