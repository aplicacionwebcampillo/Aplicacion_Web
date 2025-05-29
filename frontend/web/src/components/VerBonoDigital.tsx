import { useEffect, useState } from "react";

interface BonoDigital {
  dni: string;
  num_socio: string;
  tipo_membresia: string;
  temporada: string;
  fecha_inicio: string;
  fecha_fin: string;
  perfil_url?: string | null;
}

export default function VerBonoDigital() {
  const [bono, setBono] = useState<BonoDigital | null>(null);
  const [error, setError] = useState<string | null>(null);
  const dni = localStorage.getItem("dni");
  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchBono = async () => {
      if (!dni || !token) {
        setError("No hay sesión activa.");
        return;
      }

      try {
        const res = await fetch(
          `http://localhost:8000/socio_abonos/socio/${dni}/abono_digital`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (res.ok) {
          const textData = await res.text();
          const parsedBono = JSON.parse(textData);
          setBono(parsedBono);
        } else {
          setError("No se pudo obtener el abono digital.");
        }
      } catch (err) {
        console.error("Error al obtener bono digital:", err);
        setError("Ocurrió un error al consultar el abono.");
      }
    };

    fetchBono();
  }, [dni, token]);

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      <h2 className="text-xl font-semibold mb-4 text-center">Abono Digital</h2>

      {error && <p className="text-red-500 text-center">{error}</p>}

      {bono ? (
        <div className="bg-blanco text-negro_texto rounded-[1rem] shadow-md p-6 space-y-3 font-poetsen font-bold">
          {bono.foto_perfil && (
            <div className="flex justify-center mb-4">
              <img
                src={bono.foto_perfil}
                alt="Foto de perfil del socio"
                className="w-[10rem] h-auto rounded-full object-cover border-4 border-cyan-500"
              />
            </div>
          )}
          <p><span className="font-semibold">DNI:</span> {bono.dni}</p>
          <p><span className="font-semibold">Número de Socio:</span> {bono.num_socio}</p>
          <p><span className="font-semibold">Tipo de Membresía:</span> {bono.tipo_membresia}</p>
          <p><span className="font-semibold">Temporada:</span> {bono.temporada}</p>
          <p><span className="font-semibold">Fecha Inicio:</span> {bono.fecha_inicio}</p>
          <p><span className="font-semibold">Fecha Fin:</span> {bono.fecha_fin}</p>
          
          <h2 className="font-semibold text-negro text-center"> UN PUEBLO, UN EQUIPO, UNA FAMILIA</h2>
        </div>
      ) : (
        !error && <p className="text-center">Cargando abono...</p>
      )}
    </div>
  );
}

