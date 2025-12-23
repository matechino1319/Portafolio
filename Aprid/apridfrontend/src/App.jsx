import "./App.css"
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login.jsx";
import Home from "./pages/Home.jsx";
import Recibo from "./pages/Recibo.jsx";
import Gestion from "./pages/Gestion.jsx";
import Informe from "./pages/Informe.jsx";
import Ajustes from "./pages/Ajustes.jsx";
import Agregar from "./pages/Agregar.jsx";
import Editar from "./pages/Editar.jsx";
import { AjustesProvider } from "./context/AjustesContext.jsx";

function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <AjustesProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<PrivateRoute><Home/></PrivateRoute>}/>
        <Route path="/recibo" element={<PrivateRoute><Recibo /></PrivateRoute>}/>
        <Route path="/gestion" element={<PrivateRoute><Gestion /></PrivateRoute>}/>
        <Route path="/informe" element={<PrivateRoute><Informe /></PrivateRoute>}/>
        <Route path="/ajustes" element={<PrivateRoute><Ajustes /></PrivateRoute>}/>
        <Route path="/agregar" element={<PrivateRoute><Agregar /></PrivateRoute>}/>
        <Route path="/editar/:dni" element={<PrivateRoute><Editar /></PrivateRoute>}/>
      </Routes>
    </AjustesProvider>
  );
}

export default App;
