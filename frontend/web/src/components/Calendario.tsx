import { useEffect, useState } from "react";

function useWindowWidth() {
  const [width, setWidth] = useState<number | null>(null);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return width;
}

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

const FILAS_POR_PAGINA = 3;
const COLUMNAS = 3;
const PARTIDOS_POR_PAGINA = FILAS_POR_PAGINA * COLUMNAS;

export default function TodosPartidos() {
  const [categoriaActiva, setCategoriaActiva] = useState<
    "Senior" | "Femenino" | "Juvenil" | "Todos"
  >("Todos");
  const [partidos, setPartidos] = useState<Partido[]>([]);
  const [paginaActual, setPaginaActual] = useState(1);

  const width = useWindowWidth();

  useEffect(() => {
    const temporada_competicion = "Temporada 2024-2025";

    async function fetchAllPartidos() {
      try {
        let competicionesAConsultar: string[] = [];

        if (categoriaActiva === "Todos") {
          competicionesAConsultar = Object.values(competicionesPorCategoria).flat();
        } else {
          competicionesAConsultar = competicionesPorCategoria[categoriaActiva];
        }

        const fetches = competicionesAConsultar.map((competicion) =>
          fetch(
            `https://aplicacion-web-m5oa.onrender.com/partidos/?nombre_competicion=${encodeURIComponent(
              competicion
            )}&temporada_competicion=${encodeURIComponent(temporada_competicion)}`
          ).then((res) => res.json() as Promise<Partido[]>)
        );

        const resultados = await Promise.all(fetches);
        const todosPartidos = resultados.flat();

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

  // Resetear página cuando cambia categoría
  useEffect(() => {
    setPaginaActual(1);
  }, [categoriaActiva]);

  const totalPaginas = Math.ceil(partidos.length / PARTIDOS_POR_PAGINA);

  const partidosPagina = partidos.slice(
    (paginaActual - 1) * PARTIDOS_POR_PAGINA,
    paginaActual * PARTIDOS_POR_PAGINA
  );

  const cambiarPagina = (direccion: "anterior" | "siguiente") => {
    setPaginaActual((prev) => {
      if (direccion === "anterior" && prev > 1) return prev - 1;
      if (direccion === "siguiente" && prev < totalPaginas) return prev + 1;
      return prev;
    });
  };

  if (width === null) return null;

  return (
    <section className="md:w-[101%] bg-celeste text-black px-4 py-8 text-blanco rounded-[1rem] font-bold font-poetsen">
      <h2 className="text-2xl font-bold mb-6 text-center">Calendario</h2>

      {/* Botones categoría */}
      <div className="flex justify-center gap-4 mb-6">
        {(["Todos", "Senior", "Femenino", "Juvenil"] as const).map((cat) => (
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

      {/* Lista de Partidos (paginados) */}
      <div className="w-[99%] grid gap-6 sm:grid-cols-2 lg:grid-cols-3 justify-center">
        {partidosPagina.length === 0 && (
          <p className="text-center text-gray-500 col-span-2">
            No hay partidos disponibles para esta selección.
          </p>
        )}

        {partidosPagina.map((partido, index) => {
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
              className="bg-blanco rounded-[1rem] min-w-[19rem] max-w-[19rem] md:min-w-[24rem] md:max-w-[24rem] shadow-md p-4 text-negro"
            >
              {/* Competición */}
              <div className="text-center text-sm space-y-1 mb-2">
                <p className="text-negro_texto">{partido.nombre_competicion}</p>
              </div>

              {/* Jornada */}
              <div className="text-center text-sm space-y-1 mb-2">
                <p className="text-negro_texto">Jornada {partido.jornada}</p>
              </div>

              {/* Equipos y resultado */}
              <div className="flex justify-between items-center font-semibold mb-2">
                <div className="w-1/3 text-left">{partido.local}</div>
                <div className="w-1/3 text-center text-2xl font-bold">
                  {mostrarResultado
                    ? `${partido.resultado_local} - ${partido.resultado_visitante}`
                    : "vs"}
                </div>
                <div className="w-1/3 text-right">{partido.visitante}</div>
              </div>

              {/* Fecha y hora */}
              <div className="text-center text-sm space-y-1">
                <p className="text-negro_texto">{fechaFormateada}</p>
                {partido.hora?.match(/^\d{2}:\d{2}:\d{2}$/) && (
                  <p className="text-negro_texto">{partido.hora.slice(0, 5)}</p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Paginación */}
      {totalPaginas > 1 && (
        <div className="flex justify-center items-center gap-6 mt-10">
          <button
            onClick={() => cambiarPagina("anterior")}
            disabled={paginaActual === 1}
            className={`text-2xl px-3 py-1 rounded-full border ${
              paginaActual === 1
                ? "text-gray-400 border-gray-300 cursor-not-allowed"
                : "text-azul border-azul bg-blanco hover:bg-azul hover:text-blanco"
            }`}
          >
            ←
          </button>
          <span className="text-lg font-bold">
            {paginaActual} / {totalPaginas}
          </span>
          <button
            onClick={() => cambiarPagina("siguiente")}
            disabled={paginaActual === totalPaginas}
            className={`text-2xl px-3 py-1 rounded-full border ${
              paginaActual === totalPaginas
                ? "text-gray-400 border-gray-300 cursor-not-allowed"
                : "text-azul border-azul bg-blanco hover:bg-azul hover:text-blanco"
            }`}
          >
            →
          </button>
        </div>
      )}
    </section>
  );
}

