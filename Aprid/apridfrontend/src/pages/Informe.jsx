import "../styles/informe.css";
import { useAjustes } from "../context/AjustesContext.jsx";
import Header from "../components/Header.jsx";
import EditarModal from "../components/EditarModal.jsx";
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

function Informe() {
  const { ajustes } = useAjustes();
  const [recibos, setRecibos] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [estado, setEstado] = useState("");
  const [editando, setEditando] = useState(null);
  const limpiarFiltros = () => {
    setBusqueda("");
    setDesde("");
    setHasta("");
    setEstado("");
  };

  const location = useLocation();

useEffect(() => {
  const fetchRecibos = async () => {
    try {
      const res = await fetch("http://localhost:3000/recibos");
      if (!res.ok) throw new Error("Error al obtener los recibos");
      const data = await res.json();

      const params = new URLSearchParams(location.search);
      const dni = params.get("dni");
      console.log(dni);

      if (dni) {
        const filtrados = data.filter(r => String(r.dni_alumno) === dni);
        setRecibos(filtrados);
        setBusqueda(dni); 
      } else {
        setRecibos(data);
      }

    } catch (err) {
      console.error(err);
    }
  };

  fetchRecibos();
}, [location.search]);

  const calcularEstado = (r) => {

    const pagado = Number(r.monto_pagado) || 0;
    const total = Number(r.monto_total) || 0;

    if (pagado > total) return "pago de más";
    if (pagado >= total) return "al día";
    if (pagado < total) return "pago parcial";
  };


  const filtrados = recibos.filter((r) => {
    const texto = busqueda.toLowerCase();
    const fechaRecibo = new Date(r.fecha_pago);

    const desdeDate = desde ? new Date(desde) : null;
    const hastaDate = hasta ? new Date(hasta) : null;

    const estadoCalc = calcularEstado(r);

    const coincideTexto =
      r.nombre?.toLowerCase().includes(texto) ||
      r.apellido?.toLowerCase().includes(texto) ||
      r.dni_alumno?.toString().includes(texto);

    const coincideFecha =
      (!desdeDate || fechaRecibo >= desdeDate) &&
      (!hastaDate || fechaRecibo <= hastaDate);

    const coincideEstado =
      !estado ||
      (estado === "aldia" && estadoCalc === "al día") ||
      (estado === "parcial" && estadoCalc === "pago parcial") ||
      (estado === "mas" && estadoCalc === "pago de más");

    return coincideTexto && coincideFecha && coincideEstado;
  });

  const handleEditar = (recibo) => setEditando(recibo);

  const handleBorrar = async (id) => {
    if (!confirm("¿Seguro que querés borrar este recibo?")) return;

    try {
      await fetch(`http://localhost:3000/recibos/${id}`, {
        method: "DELETE",
      });

      setRecibos((prev) => prev.filter((r) => r.id_comprobante !== id));
    } catch (err) {
      alert("No se pudo borrar el recibo");
    }
  };

  const actualizarRecibo = async () => {
    const res = await fetch("http://localhost:3000/recibos");
    const data = await res.json();
    setRecibos(data);
    setEditando(null);
  };

  return (
    <>
      <Header />
      <main
        className="general-container"
        style={{ fontSize: `${ajustes.tamano}px`, color: ajustes.colores.letra }}
      >
        <h1>Informe de Pagos</h1>

       <section className="filtros">

  <div className="filtros-grid">

    <div className="filtro-item">
      <label>Buscar</label>
      <input
        type="text"
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
        placeholder="Nombre o DNI"
      />
    </div>

    <div className="filtro-item">
      <label>Estado</label>
      <select value={estado} onChange={(e) => setEstado(e.target.value)}>
        <option value="">Todos</option>
        <option value="aldia">Al día</option>
        <option value="parcial">Pago parcial</option>
        <option value="mas">Pago de más</option>
      </select>
    </div>

    <div className="filtro-item">
      <label>Desde</label>
      <input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
    </div>

    <div className="filtro-item">
      <label>Hasta</label>
      <input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />
    </div>

  </div>

  <button onClick={limpiarFiltros} className="btn-limpiar">
    Limpiar filtros
  </button>

</section>


        <section className="tabla">
          <table>
            <thead>
              <tr>
                <th>Alumno</th>
                <th>DNI</th>
                <th>Fecha pago</th>
                <th>Pagado / Total</th>
                <th>Estado</th>
                <th>Herramientas</th>
              </tr>
            </thead>

            <tbody>
              {filtrados.length > 0 ? (
                filtrados.map((r) => {
                  const estadoCalc = calcularEstado(r);

                  return (
                    <tr key={r.id_comprobante}>
                      <td>{r.nombre} {r.apellido}</td>
                      <td>{r.dni_alumno}</td>
                      <td>{new Date(r.fecha_pago).toLocaleDateString()}</td>
                      <td>
                        {(() => {
                          const pagado = Number(r.monto_pagado) || 0;
                          const total = Number(r.monto_total) || 0;
                          const diff = pagado - total;

                          if (diff > 0)
                            return `$${pagado.toFixed(2)} (+$${diff.toFixed(2)})`;

                          if (diff === 0)
                            return `$${pagado.toFixed(2)} / $${total.toFixed(2)}`;

                          return `$${pagado.toFixed(2)} (faltan $${Math.abs(diff).toFixed(2)})`;
                        })()}
                      </td>

                      <td
                        style={{
                          color:
                            estadoCalc === "al día" ? "green" :
                              estadoCalc === "pago de más" ? "blue" :
                                  "#b8860b",
                        }}
                      >
                        {estadoCalc}
                      </td>

                      <td>
                        <button onClick={() => handleEditar(r)}>✏️</button>
                        <button onClick={() => handleBorrar(r.id_comprobante)}>🗑️</button>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan="6" className="mensaje-vacio">
                    No hay recibos cargados todavía
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </section>

        {editando && (
          <EditarModal recibo={editando} onClose={() => setEditando(null)} onSave={actualizarRecibo} />
        )}
      </main>
    </>
  );
}

export default Informe;
