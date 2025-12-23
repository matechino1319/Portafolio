import { createContext, useState, useEffect, useContext } from "react";

// Crear el contexto
const AjustesContext = createContext();

// Proveedor del contexto
export function AjustesProvider({ children }) {
  const [ajustes, setAjustes] = useState(
  {
    colores: {
      barraLateral: "#ffffff",
      botones: "#0187C4",
      letra: "#000000",
      logo: "#0187C4",
      
    },
    monto:15000,
    tamano: 16,
    tema: "claro",
  });

  // Cargar ajustes guardados desde localStorage
  useEffect(() => {
    const guardado = JSON.parse(localStorage.getItem("ajustes"));
    if (guardado) {
  setAjustes((prev) => ({
    ...prev,
    ...guardado,
  }));
}

  }, []);

  // Guardar ajustes cada vez que cambien
  useEffect(() => {
    localStorage.setItem("ajustes", JSON.stringify(ajustes));
    document.body.classList.remove("claro", "oscuro");
    document.body.classList.add(ajustes.tema);
  }, [ajustes]);

  return (
    <AjustesContext.Provider value={{ ajustes, setAjustes }}>
      {children}
    </AjustesContext.Provider>
  );
}

// Hook personalizado para usar el contexto
export function useAjustes() {
  return useContext(AjustesContext);
}

