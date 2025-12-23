import { useState } from "react";
import "../styles/login.css";
import { useNavigate } from "react-router-dom";
import logoAprid from "../assets/logo_aprid.png";
function Login() {
  const [usuario, setUsuario] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:3000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, password }),
      });
      if (!res.ok) throw new Error("Credenciales incorrectas");

      const data = await res.json();
      localStorage.setItem("token", data.token);
      navigate("/gestion");
    } catch (error) {
      alert("Usuario o contraseña incorrectos");
    }
  };

  return (
    <div className="login-wrapper">

      <div className="wrapper">
        <img src={logoAprid} alt="" />
        <form onSubmit={handleLogin}>
          <div className="input-box">
            <input
              type="text"
              id="usuario"
              name="usuario"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
              required
            />
            <label htmlFor="usuario">Usuario</label>
          </div>

          <div className="input-box">
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <label htmlFor="password">Contraseña</label>
          </div>

          <div className="forgot">
            <a href="#">¿Olvidaste tu contraseña?</a>
          </div>

          <button className="btn" type="submit">
            Ingresar
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
