import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Usuario from "../components/Usuario";
import Administrador from "../components/Administrador";
import Socios from "../components/Socios";
import Productos from "../components/Productos";
import Noticias from "../components/NoticiasAdmin";
import Patrocinadores from "../components/PatrocinadoresAdmin";
import Jugadores from "../components/Jugadores";
import Equipos from "../components/Equipos";
import Abonos from "../components/Abonos";
import ValidarPago from "../components/ValidarPago";


export default function AdministradorPage() {
  const navigate = useNavigate();
  const [seccion, setSeccion] = useState<string>("modificar");
  const [adminData, setAdminData] = useState<null | {
    cargo: string;
    permisos: string;
    estado: string;
    foto_perfil: string;
  }>(null);

  const dni = localStorage.getItem("dni") || "";
  const token = localStorage.getItem("token") || "";

  useEffect(() => {
    if (!token || !dni) return;

    const fetchAdministrador = async () => {
      try {
        const res = await fetch(`http://localhost:8000/administradores/${dni}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
          const data = await res.json();
          setAdminData({
            cargo: data.cargo,
            permisos: data.permisos,
            estado: data.estado,
            foto_perfil: data.foto_perfil,
          });
        }
      } catch (err) {
        console.error("Error al obtener administrador:", err);
      }
    };

    fetchAdministrador();
  }, [dni, token]);

  const botones = [
    { id: "usuarios", label: "Usuarios" },
    { id: "administrador", label: "Administradores" },
    { id: "socios", label: "Socios" },
    { id: "productos", label: "Productos" },
    { id: "noticias", label: "Noticias" },
    { id: "patrocinadores", label: "Patrocinadores" },
    { id: "jugadores", label: "Jugadores" },
    { id: "equipos", label: "Equipos" },
    { id: "abonos", label: "Abonos" },
    { id: "validarPago", label: "Validar Pagos" },
  ];

  return (
    <div className="flex flex-col md:flex-row bg-gray-50">
      {/* Menú lateral */}
      {adminData && (
        <aside className="bg-celeste text-white h-auto px-6 py-10 rounded-[1rem] font-poetsen font-bold md:w-full max-w-full m-[1.5rem] md:max-w-[20rem] md:w-1/4 flex flex-col justify-center items-center md:items-start space-y-4">
          <button
            onClick={() => navigate("/usuario")}
            className="w-full max-w-xs px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
          >
            Zona Usuario
          </button>

          {botones.map((btn) => (
            <button
              key={btn.id}
              onClick={() => setSeccion(btn.id)}
              className={`w-full max-w-xs px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco ${
                seccion === btn.id ? "" : ""
              }`}
            >
              {btn.label}
            </button>
          ))}
        </aside>
      )}

      {/* Contenido derecho */}
      <main className="flex-1 p-6 flex justify-center items-start">
        {seccion === "usuarios" && adminData && <Usuario />}
        {seccion === "administrador" && <Administrador />}
        {seccion === "socios" && <Socios />}
        {seccion === "productos" && <Productos />}
        {seccion === "noticias" && <Noticias />}
        {seccion === "patrocinadores" && <Patrocinadores />}
        {seccion === "jugadores" && <Jugadores />}
        {seccion === "equipos" && <Equipos />}
        {seccion === "abonos" && <Abonos />}
        {seccion === "validarPago" && <ValidarPago />}
      </main>
    </div>
  );
}

