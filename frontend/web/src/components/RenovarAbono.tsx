import { useEffect, useState } from "react";

interface Abono {
  id_abono: number;
  temporada: string;
  precio: number;
  fecha_inicio: string;
  fecha_fin: string;
  descripcion: string;
}

export default function RenovarAbono() {
  const dni = localStorage.getItem("dni") || "";
  const token = localStorage.getItem("token");

  const [abonos, setAbonos] = useState<Abono[]>([]);
  const [idSeleccionado, setIdSeleccionado] = useState<number | null>(null);
  const [mensaje, setMensaje] = useState<string | null>(null);

  useEffect(() => {
    const fetchAbonos = async () => {
      try {
        const res = await fetch("http://localhost:8000/abonos/");
        if (res.ok) {
          const data = await res.json();
          setAbonos(data);
        } else {
          throw new Error("Error al obtener abonos.");
        }
      } catch (error: any) {
        console.error(error);
        setMensaje(`❌ ${error.message}`);
      }
    };

    fetchAbonos();
  }, []);

  const handleRenovar = async () => {
    if (!dni || !token || !idSeleccionado) {
      setMensaje("❌ Faltan datos para renovar el abono.");
      return;
    }

    try {
      const res = await fetch(`http://localhost:8000/socio_abonos/renovar/${dni}/${idSeleccionado}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        const data = await res.text();
        setMensaje(`✅ ${data}`);
      } else {
        const errorText = await res.text();
        throw new Error(errorText);
      }
    } catch (error: any) {
      setMensaje(`❌ Error: ${error.message}`);
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      <h2 className="text-2xl font-bold text-blanco text-center">Renovar Abono</h2>

      <div className="space-y-4">
        <label className="block text-gray-700 font-semibold">Selecciona un abono:</label>
        <select
          className="rounded-[1rem] font-poetsen w-[90%] bg-blanco border-2 border-azul px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          value={idSeleccionado ?? ""}
          onChange={(e) => setIdSeleccionado(Number(e.target.value))}
        >
          <option value="" disabled>-- Selecciona un abono --</option>
          {abonos.map((abono) => (
            <option key={abono.id_abono} value={abono.id_abono}>
              {abono.temporada} - Id_Abono: {abono.id_abono} - ({abono.precio} €)
            </option>
          ))}
        </select>
	
	<div className="flex justify-center">
        <button
          onClick={handleRenovar}
          className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Renovar Abono
        </button>

        {mensaje && <p className="text-center font-medium">{mensaje}</p>}
        </div>
      </div>
    </div>
  );
}

