import { useEffect, useState } from "react";

interface Clasificacion {
  nombre_competicion: string;
  temporada_competicion: string;
  equipo: string;
  posicion: number;
  puntos: number;
}

interface ResultadoPartido {
  local: string;
  visitante: string;
  goles_local: string;
  goles_visitante: string;
  fecha?: string | null;
  hora?: string | null;
}

interface ResultadoResponse {
  jornada: string | null;
  partidos: ResultadoPartido[];
}

const competiciones: Record<string, string> = {
  Senior: "2ª Andaluza Sénior (Jaén)",
  Femenino_7: "Liga Femenina Sénior Fútbol 7 (Jaén)",
  Femenino_11: "2ª Andaluza Femenina Sénior (Jaén)",
};

const now = new Date();
const year = now.getFullYear();
const month = now.getMonth() + 1;
const startYear = month >= 8 ? year : year - 1;
const endYear = startYear + 1;

export default function Clasificacion() {
  const [datos, setDatos] = useState<Clasificacion[]>([]);
  const [categoriaActiva, setCategoriaActiva] = useState<
    "Senior" | "Femenino_7" | "Femenino_11"
  >("Senior");

  const [resultados, setResultados] = useState<ResultadoPartido[]>([]);
  const [jornadaActual, setJornadaActual] = useState<string | null>(null);

  useEffect(() => {
    const nombre_competicion = competiciones[categoriaActiva];
    const temporada_competicion = `Temporada ${startYear}-${endYear}`;

    // 🔹 1️⃣ Fetch clasificación
    fetch(
      `https://aplicacion-web-m5oa.onrender.com/clasificaciones?nombre_competicion=${encodeURIComponent(
        nombre_competicion
      )}&temporada_competicion=${encodeURIComponent(temporada_competicion)}`
    )
      .then((res) => res.json())
      .then((data) => setDatos(data))
      .catch((err) => console.error("Error al cargar la clasificación:", err));

    // 🔹 2️⃣ Fetch resultados desde la BD (nuevo backend)
    const urlResultados = import.meta.env.PROD
      ? `https://aplicacion-web-m5oa.onrender.com/resultados?categoria=${categoriaActiva}`
      : `http://localhost:8000/resultados?categoria=${categoriaActiva}`;

    fetch(urlResultados)
      .then((res) => res.json())
      .then((data: ResultadoResponse) => {
        setResultados(data.partidos);
        setJornadaActual(data.jornada);
      })
      .catch((err) => {
        console.error("Error al cargar resultados:", err);
        setResultados([]);
        setJornadaActual(null);
      });
  }, [categoriaActiva]);

  return (
    <section className="bg-celeste text-black px-4 py-8 text-blanco rounded-[1rem] font-bold font-poetsen">
      <h2 className="text-2xl font-bold mb-6 text-center">Clasificación</h2>

      {/* Botones de categoría */}
      <div className="flex justify-center gap-4 mb-6">
        {([
          { key: "Senior", label: "Senior" },
          { key: "Femenino_7", label: "Femenino Fútbol 7" },
          { key: "Femenino_11", label: "Femenino Fútbol 11" },
        ] as const).map(({ key, label }) => (
          <button
            key={key}
            onClick={() => setCategoriaActiva(key)}
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 ${
              categoriaActiva === key
                ? "bg-azul text-blanco border-azul"
                : "bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            }`}
          >
            {label}
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
                    fila.equipo.includes("C.D. CAMPILLO DEL RÍO")
                      ? "bg-green-200 text-azul"
                      : ""
                  }`}
                >
                  <td className="px-4 py-2 md:pl-[5rem] border-t">
                    {fila.posicion}
                  </td>
                  <td className="px-4 py-2 md:pl-[11rem] border-t">
                    {fila.equipo}
                  </td>
                  <td className="px-4 py-2 md:pl-[3rem] border-t">
                    {fila.puntos}
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {/* RESULTADOS */}
      <div className="mt-8">
        <h3 className="text-xl font-bold mb-4 text-center">
          Resultados - Última Jornada
        </h3>

        {resultados.length === 0 ? (
          <p className="text-center text-gray-500">Cargando resultados...</p>
        ) : (
          <div className="flex flex-col gap-3 max-w-3xl mx-auto">
            {jornadaActual && (
              <p className="text-center text-sm text-gray-600 mb-2">
                {jornadaActual}
              </p>
            )}
            {resultados.map((p, i) => (
              <div
                key={i}
                className="flex justify-between items-center bg-blanco text-negro rounded-[1rem] p-3 shadow-md"
              >
                <span className="w-1/3 text-right font-semibold">{p.local}</span>
                <span className="w-1/3 text-center text-lg font-bold">
                  {p.goles_local} - {p.goles_visitante}
                </span>
                <span className="w-1/3 text-left font-semibold">{p.visitante}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

