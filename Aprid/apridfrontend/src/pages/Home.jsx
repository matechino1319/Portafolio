import { Link } from "react-router-dom";
import "../styles/home.css";

function Home() {
  return (
    <>
     <header className="main-header">
        <h1>Aprid</h1>
        <div className="profile-pic"></div>
      </header>
      <main className="main-content">
        <Link to="/recibo" className="card">Emitir recibo</Link>
        <Link to="/gestion" className="card">Gestión de alumnos</Link>
        <Link to="/informe" className="card">Informe</Link>
        <Link to="/ajustes" className="card">Ajustes</Link>
      </main>
    </>
  );
}

export default Home;
