import { useEffect, useState } from "react";

interface Partido {
  nombre_competicion: string;
  temporada_competicion: string;
  local: string;
  visitante: string;
  dia: string;
  hora: string;
  jornada: string;
  resultado_local: number;
  resultado_visitante: number;
  acta: string;
}

const competicionesPorCategoria: Record<string, string[]> = {
  Senior: [
    "2ª Andaluza Sénior (Jaén)",
    "Fase Final 2ª Andaluza Sénior (Jaén)",
    "Copa Andalucía 2ª Andaluza Sénior (Jaén)",
    "Trofeo Copa Subdelegado del Gobierno (Jaén)",
    "Fase Final Trofeo Copa Subdelegado del Gobierno (Jaén)",
  ],
  Femenino: ["Liga Fomento Femenino Sénior Fútbol 7 (Jaén)"],
  Juvenil: ["3ª Andaluza Juvenil (Jaén)"],
};

export default function TodosPartidos() {
  const [categoriaActiva, setCategoriaActiva] = useState<
    "Senior" | "Femenino" | "Juvenil" | "Todos"
  >("Todos");
  const [partidos, setPartidos] = useState<Partido[]>([]);

  useEffect(() => {
    const temporada_competicion = "Temporada 2024-2025";

    async function fetchAllPartidos() {
      try {
        let competicionesAConsultar: string[] = [];

        if (categoriaActiva === "Todos") {
          // Todas las competiciones de todas las categorías
          competicionesAConsultar = Object.values(competicionesPorCategoria).flat();
        } else {
          competicionesAConsultar = competicionesPorCategoria[categoriaActiva];
        }

        const fetches = competicionesAConsultar.map((competicion) =>
          fetch(
            `http://localhost:8000/partidos/?nombre_competicion=${encodeURIComponent(
              competicion
            )}&temporada_competicion=${encodeURIComponent(temporada_competicion)}`
          ).then((res) => res.json() as Promise<Partido[]>)
        );

        const resultados = await Promise.all(fetches);
        const todosPartidos = resultados.flat();

        // Ordenar por fecha ascendente
        todosPartidos.sort(
          (a, b) => new Date(a.dia).getTime() - new Date(b.dia).getTime()
        );

        setPartidos(todosPartidos);
      } catch (error) {
        console.error("Error cargando partidos:", error);
        setPartidos([]);
      }
    }

    fetchAllPartidos();
  }, [categoriaActiva]);

  return (
    <section className="bg-celeste text-black px-4 py-8 text-blanco rounded-[1rem] font-bold font-poetsen">
      <h2 className="text-2xl font-bold mb-6 text-center">Calendario</h2>

      {/* Botones categoría */}
      <div className="flex justify-center gap-4 mb-6">
        {(["Todos", "Senior", "Femenino", "Juvenil"] as const).map((cat) => (
          <button
            key={cat}
            onClick={() => setCategoriaActiva(cat)}
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 ${
              categoriaActiva === cat
                ? "bg-rojo text-blanco border-rojo"
                : "bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Lista de Partidos */}
      <div className="grid gap-6 sm:grid-cols-2">
        {partidos.length === 0 && (
          <p className="text-center text-gray-500 col-span-2">
            No hay partidos disponibles para esta selección.
          </p>
        )}

        {partidos.map((partido, index) => {
          const fecha = new Date(partido.dia);
          const dia = String(fecha.getDate()).padStart(2, "0");
          const mes = String(fecha.getMonth() + 1).padStart(2, "0");
          const anio = fecha.getFullYear();
          const fechaFormateada = `${dia}/${mes}/${anio}`;
          
          const ahora = new Date();
          const fechaPartido = new Date(`${partido.dia}T${partido.hora}`);
          const mostrarResultado = fechaPartido < ahora;

          return (
            <div
              key={index}
              className="bg-blanco rounded-[1rem] min-w-[19rem] max-w-[19rem] md:min-w-[24rem] md:max-w-[24rem] shadow-md rounded-lg p-4 max-w-2xl mx-auto text-negro"
            >
              {/* Competición */}
              <div className="text-center text-sm text-gray-600 space-y-1 mb-2">
                <p className="italic">{partido.nombre_competicion}</p>
              </div>

              {/* Jornada */}
              <div className="text-center text-sm text-gray-600 space-y-1 mb-2">
                <p>Jornada {partido.jornada}</p>
              </div>

              {/* Equipos y resultado */}
              <div className="flex justify-between items-center text-white font-semibold mb-2">
                <div className="w-1/3 text-left text-black">{partido.local}</div>
                <div className="w-1/3 text-center text-black text-2xl font-bold">
                  {mostrarResultado
                    ? `${partido.resultado_local} - ${partido.resultado_visitante}`
                    : "vs"}
                </div>
                <div className="w-1/3 text-right text-black">{partido.visitante}</div>
              </div>

              {/* Fecha y hora */}
              <div className="text-center text-sm text-gray-600 space-y-1">
                <p>{fechaFormateada}</p>
                {partido.hora?.match(/^\d{2}:\d{2}:\d{2}$/) && (
                  <p>{partido.hora.slice(0, 5)}</p>
                )}
              </div>
            </div>
          );
        })}
      </div>
      
    </section>
  );
}

