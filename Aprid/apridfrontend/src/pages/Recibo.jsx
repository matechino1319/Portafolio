import "../styles/recibo.css";
import { useAjustes } from "../context/AjustesContext.jsx";
import Header from "../components/Header.jsx";
import { useState, useEffect } from "react";

const API_URL = "http://localhost:3000/whatsapp/status";
const POLLING_INTERVAL = 5000;

function Recibo() {
  const { ajustes } = useAjustes();

  const [formData, setFormData] = useState({
    nombre: "",
    dni_alumno: "",
    monto_pagado: "",
    monto_total: ajustes.monto,
    fecha_pago: "",
    cuotaInicio: "",
    cuotaFin: "",
    descripcion: "",
  });

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:3000/recibos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error("Error al guardar el recibo");
      alert("Recibo guardado correctamente");

      setFormData({
        nombre: "",
        dni_alumno: "",
        monto_pagado: "",
        fecha_pago: "",
        cuotaInicio: "",
        cuotaFin: "",
        descripcion: "",
      });
    } catch (error) {
      console.error(error);
      alert("Ocurrió un error al guardar el recibo");
    }
  };

  const [status, setStatus] = useState("INICIALIZANDO");
  const [qrCode, setQrCode] = useState(null);

  const fetchStatus = async () => {
    try {
      const res = await fetch(API_URL);
      const data = await res.json();
      setStatus(data.status);
      setQrCode(data.qr || null);
    } catch (err) {
      console.error("Error al obtener estado:", err);
      setStatus("ERROR_CONEXION");
      setQrCode(null);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, POLLING_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  return(
    <>
      <Header />
      <div className="general-container" style={{ fontSize: `${ajustes.tamano}px `}}>
        <h1>Nuevo Recibo</h1>

        <div className="flex flex-col items-center justify-center p-4 bg-gray-100 rounded-lg shadow-md mb-4">
          <h2 className="text-xl font-bold mb-2">Estado WhatsApp: {status}</h2>

          {qrCode && status === "WAITING_QR" && (
            <div style={{ width: 200, height: 200 }}>
              <img
                src={`https://api.qrserver.com/v1/create-qr-code/?data=${encodeURIComponent(qrCode)}&size=200x200`}
                alt="QR WhatsApp"
              />
            </div>
          )}

          {status === "CONNECTED" && (
            <p className="text-green-600 font-semibold mt-2">Cliente conectado ✅</p>
          )}

          {status === "ERROR_CONEXION" && (
            <p className="text-red-600 font-semibold mt-2">Error de conexión ❌</p>
          )}
        </div>

        <form onSubmit={handleSubmit} className="recibo-form">
          <label>
            Nombre:
            <input
              type="text"
              id="nombre"
              value={formData.nombre}
              onChange={handleChange}
              placeholder="Pablo Silva"
            />
          </label>

          <label>
            DNI del alumno:
            <input
              type="number"
              id="dni_alumno"
              value={formData.dni_alumno}
              onChange={handleChange}
              placeholder="39438262"
            />
          </label>

          <label>
            Monto:
            <input
              type="number"
              id="monto_pagado"
              value={formData.monto_pagado}
              onChange={handleChange}
              placeholder="10000"
            />
          </label>

          <label>
            Fecha de pago:
            <input
              type="date"
              id="fecha_pago"
              value={formData.fecha_pago}
              onChange={handleChange}
            />
          </label>

          <label className="cuota-label">
            Cuota (inicio / fin):
            <div className="cuota-duo">
              <input
                type="month"
                id="cuotaInicio"
                value={formData.cuotaInicio}
                onChange={handleChange}
              />
              <input
                type="month"
                id="cuotaFin"
                value={formData.cuotaFin}
                onChange={handleChange}
              />
            </div>
          </label>

          <label className="textarea-label">
            Items / descripción:
            <textarea
              id="descripcion"
              value={formData.descripcion}
              onChange={handleChange}
              placeholder="Escribe aquí los ítems..."
            ></textarea>
          </label>

          <button
            type="submit"
            className="recibo-btn"
            style={{
              backgroundColor: ajustes.colores.botones,
              color: ajustes.colores.letra,
            }}
          >
            Guardar recibo
          </button>
        </form>
      </div>
    </>
  )
}

export default Recibo;