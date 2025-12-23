import "../styles/modal.css";
import { useState } from "react";
import { useAjustes } from "../context/AjustesContext.jsx";

function EditarModal({ recibo, onClose, onSave }) {
  const { ajustes } = useAjustes(); // ← usar el contexto
  const [formData, setFormData] = useState({
    dni_alumno: recibo.dni_alumno,
    monto_pagado: recibo.monto_pagado,
    fecha_pago: recibo.fecha_pago.split("T")[0],
    descripcion: recibo.descripcion,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`http://localhost:3000/recibos/${recibo.id_comprobante}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error("Error al actualizar");
      const actualizado = await res.json();
      onSave(actualizado);
    } catch (err) {
      console.error(err);
      alert("No se pudo editar el recibo");
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
        <h2 style={{ color: ajustes.colores.logo }}>Editar Recibo</h2>

        <label>DNI del alumno:</label>
        <input
          type="text"
          value={formData.dni_alumno}
          onChange={(e) => setFormData({ ...formData, dni_alumno: e.target.value })}
          required
        />

        <label>Monto:</label>
        <input
          type="number"
          value={formData.monto_pagado}
          onChange={(e) => setFormData({ ...formData, monto_pagado: e.target.value })}
          required
        />

        <label>Fecha de pago:</label>
        <input
          type="date"
          value={formData.fecha_pago}
          onChange={(e) => setFormData({ ...formData, fecha_pago: e.target.value })}
          required
        />

        <label>Descripción:</label>
        <textarea
          value={formData.descripcion}
          onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
        />

        <div className="acciones">
          <button
            type="submit"
            className="btn-guardar"
            style={{ background: ajustes.colores.botones }}
          >
            Guardar
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

export default EditarModal;
