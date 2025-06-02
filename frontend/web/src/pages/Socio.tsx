import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import FormularioEditarSocio from "../components/FormularioEditarSocio";
import VerBonoDigital from "../components/VerBonoDigital";
import Predicciones from "../components/Predicciones";
import CesionesAbono from "../components/CesionesAbono";
import RenovarAbono from "../components/RenovarAbono";

export function Introduccion() {
  return (
    <div className="bg-celeste text-blanco h-auto px-6 py-10 rounded-[1rem] font-poetsen font-bold md:w-full max-w-full m-[1.5rem] md:max-w-[20rem] md:w-1/4 flex flex-col justify-center items-center md:items-start space-y-4">
      <h2 className="text-2xl">Panel de Socio</h2>
      <p className="text-white text-base font-normal leading-relaxed">
        Bienvenido al panel de socio del club. Desde aquí puedes gestionar tus datos de socio, realizar cesiones de abono, las predicciones y otras funcionalidades.
      </p>
      <p className="text-white text-base font-normal leading-relaxed">
        Usa el menú de la izquierda para navegar por las diferentes secciones. Cada módulo te permite visualizar, editar o crear recursos según tus permisos.
      </p>
    </div>
  );
}
       


export default function SocioPage() {
  const navigate = useNavigate();
  const [seccion, setSeccion] = useState<string>("introduccion");
  const [socioData, setSocioData] = useState<null | {
    tipo_membresia: string;
    estado: string;
    foto_perfil: string;
  }>(null);

  const dni = localStorage.getItem("dni") || "";
  const token = localStorage.getItem("token") || "";

  useEffect(() => {
    if (!token || !dni) {
      navigate("/login");
      return;
    }

    const fetchSocio = async () => {
      try {
        const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/socios/${dni}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
          const data = await res.json();
          setSocioData({
            tipo_membresia: data.tipo_membresia,
            estado: data.estado,
            foto_perfil: data.foto_perfil,
          });
        }
      } catch (err) {
        console.error("Error al obtener socio:", err);
      }
    };

    fetchSocio();
  }, [dni, token]);

  const botones = [
    { id: "modificar", label: "Modificar Socio" },
    { id: "verAbonoDigital", label: "Ver Abono Digital" },
    { id: "predicciones", label: "Predicciones" },
    { id: "cesionesAbono", label: "Cesión de Abono" },
    { id: "renovarAbono", label: "Renovar Abono" },
  ];

  return (
    <div className="flex flex-col md:flex-row bg-gray-50 ">
      {/* Menú lateral */}
      {socioData && (
      <aside className="bg-celeste text-white h-auto px-6 py-10 rounded-[1rem] font-poetsen font-bold md:w-full max-w-full m-[1.5rem] md:max-w-[20rem]  md:w-1/4 flex flex-col justify-center items-center md:items-start space-y-4">
        <button
          onClick={() => navigate("/usuario")}
          className="w-full max-w-xs px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Zona Usuario
        </button>
        
        {botones.map((btn) => (
          <button
            key={btn.id}
            onClick={() => setSeccion(btn.id)}
            className={`w-full max-w-xs px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco ${
              seccion === btn.id
                ? ""
                : ""
            }`}
          >
            {btn.label}
          </button>
        ))}
        
      </aside>
      )}
      
      

      {/* Contenido derecho */}
      <main className="flex-1 p-6 flex justify-center items-start">
      	{seccion === "introduccion" && socioData && <Introduccion />}
        {seccion === "modificar" && <FormularioEditarSocio />}
        {seccion === "cesionesAbono" &&  <CesionesAbono />}
        {seccion === "predicciones" && <Predicciones />}
        {seccion === "renovarAbono" && <RenovarAbono />}
        {seccion === "verAbonoDigital" && <VerBonoDigital />}
        
      </main>
    </div>
  );
}

