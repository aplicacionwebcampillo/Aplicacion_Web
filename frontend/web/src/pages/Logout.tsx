import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("dni");
    window.location.reload();
    navigate("/login");
  }, [navigate]);
  
  
  return <p>Cerrando sesión...</p>;
}

