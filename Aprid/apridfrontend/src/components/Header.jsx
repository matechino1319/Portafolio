import "../styles/header.css";
import { Link } from "react-router-dom";
import { useAjustes } from "../context/AjustesContext.jsx";
import { useState } from "react";
import logoAprid from "../assets/logo_aprid.png";
function Header() {
  const { ajustes } = useAjustes();
  const [open, setOpen] = useState(false);

  return (
    <header
      className="navbar"
      style={{ backgroundColor: ajustes.colores.barraLateral }}
    >
      <div className="nav-container">
<img className="logoAprid"  src={logoAprid} alt="" />
        {open && <div className="overlay" onClick={() => setOpen(false)} />}

        <button
          className={`hamburger ${open ? "active" : ""}`}
          onClick={() => setOpen(!open)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <nav className={`sidebar ${open ? "open" : ""}`}>
          <ul  className="nav-links" >
            <li><Link to="/" onClick={() => setOpen(false)}>Inicio</Link></li>
            <li><Link to="/recibo" onClick={() => setOpen(false)}>Emitir recibo</Link></li>
            <li><Link to="/gestion" onClick={() => setOpen(false)}>Gestión de alumnos</Link></li>
            <li><Link to="/informe" onClick={() => setOpen(false)}>Informe</Link></li>
            <li><Link to="/ajustes" onClick={() => setOpen(false)}>Ajustes</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;
