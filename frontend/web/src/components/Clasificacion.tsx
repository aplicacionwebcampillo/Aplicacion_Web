import { useEffect, useState } from "react";

interface Clasificacion {
  nombre_competicion: string;
  temporada_competicion: string;
  equipo: string;
  posicion: number;
  puntos: number;
}

const competiciones: Record<string, string> = {
  Senior: "2ª Andaluza Sénior (Jaén)",
  Femenino: "Liga Fomento Femenino Sénior Fútbol 7 (Jaén)",
  Juvenil: "3ª Andaluza Juvenil (Jaén)",
};

export default function Clasificacion() {
  const [datos, setDatos] = useState<Clasificacion[]>([]);
  const [categoriaActiva, setCategoriaActiva] = useState<"Senior" | "Femenino" | "Juvenil">("Senior");

  useEffect(() => {
    const nombre_competicion = competiciones[categoriaActiva];
    const temporada_competicion = "Temporada 2024-2025";

    fetch(
      `https://aplicacion-web-m5oa.onrender.com/clasificaciones?nombre_competicion=${encodeURIComponent(
        nombre_competicion
      )}&temporada_competicion=${encodeURIComponent(temporada_competicion)}`
    )
      .then((res) => res.json())
      .then((data) => setDatos(data))
      .catch((err) => console.error("Error al cargar la clasificación:", err));
  }, [categoriaActiva]);

  return (
    <section className="bg-celeste text-black px-4 py-8 text-blanco rounded-[1rem] font-bold font-poetsen">
      <h2 className="text-2xl font-bold mb-6 text-center">Clasificación</h2>

      {/* Botones de categoría */}
      <div className="flex justify-center gap-4 mb-6">
        {(["Senior", "Femenino", "Juvenil"] as const).map((cat) => (
          <button
            key={cat}
            onClick={() => setCategoriaActiva(cat)}
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 ${
              categoriaActiva === cat
                ? "bg-azul text-blanco border-azul"
                : "bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Tabla de clasificación */}
      <div className="overflow-x-auto">
        <table className="min-w-full table-auto border-[0.2rem] border-azul bg-blanco text-negro rounded-[1rem]">
          <thead className="bg-gray-200 text-center rounded-[1rem]">
            <tr>
              <th className="px-4 py-2">Posición</th>
              <th className="px-4 py-2">Equipo</th>
              <th className="px-4 py-2">Puntos</th>
            </tr>
          </thead>
          <tbody className="text-negro_texto">
            {datos
              .sort((a, b) => a.posicion - b.posicion)
              .map((fila, index) => (
                <tr
                  key={index}
                  className={`hover:bg-gray-100 ${
                    fila.equipo === "C.D. CAMPILLO DEL RÍO C.F." ? "bg-green-200 text-azul" : ""
                  }`}
                >
                  <td className="px-4 py-2 md:pl-[5rem] border-t">{fila.posicion}</td>
                  <td className="px-4 py-2 md:pl-[11rem] border-t">{fila.equipo}</td>
                  <td className="px-4 py-2 md:pl-[3rem] border-t">{fila.puntos}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

