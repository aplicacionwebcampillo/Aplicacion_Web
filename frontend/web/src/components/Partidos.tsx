import { useEffect, useState } from "react";

interface Partido {
  nombre_competicion: string;
  temporada_competicion: string;
  local: string;
  visitante: string;
  dia: string; // fecha
  hora: string;
  jornada: string;
  resultado_local: number;
  resultado_visitante: number;
  acta: string;
}

// Define competiciones por categoría como arrays
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

export default function Partidos() {
  const [categoriaActiva, setCategoriaActiva] = useState<"Senior" | "Femenino" | "Juvenil">("Senior");
  const [ultimo, setUltimo] = useState<Partido | null>(null);
  const [proximo, setProximo] = useState<Partido | null>(null);

  useEffect(() => {
    const competiciones = competicionesPorCategoria[categoriaActiva];
    const temporada_competicion = "Temporada 2024-2025";

    // Construimos un array de fetches para cada competición
    const fetches = competiciones.map((competicion) =>
      fetch(
        `http://localhost:8000/partidos/?nombre_competicion=${encodeURIComponent(
          competicion
        )}&temporada_competicion=${encodeURIComponent(temporada_competicion)}`
      ).then((res) => res.json() as Promise<Partido[]>)
    );

    Promise.all(fetches)
      .then((resultados) => {
        // resultados es un array con arrays de partidos por competición
        const todosPartidos = resultados.flat();

        const hoy = new Date();

        const partidosOrdenados = todosPartidos.sort(
          (a, b) => new Date(a.dia).getTime() - new Date(b.dia).getTime()
        );

        const anteriores = partidosOrdenados.filter(
          (p) => new Date(p.dia) < hoy
        );
        const siguientes = partidosOrdenados.filter(
          (p) => new Date(p.dia) >= hoy
        );

        setUltimo(anteriores[anteriores.length - 1] || null);
        setProximo(siguientes[0] || null);
      })
      .catch((err) => console.error("Error cargando partidos:", err));
  }, [categoriaActiva]);

  const renderPartido = (partido: Partido | null, tipo: "próximo" | "último") => {
    if (!partido) {
      return (
        <div className="bg-white shadow-md rounded-lg p-4 text-center text-negro">
          <h3 className="text-xl font-bold mb-2 text-center">
            {tipo === "próximo" ? "Próximo Partido" : "Último Partido"}
          </h3>
          <p className="text-gray-500">
            {tipo === "próximo"
              ? "Actualmente no hay partidos programados"
              : "Actualmente no hay partidos jugados"}
          </p>
        </div>
      );
    }

    const fecha = new Date(partido.dia);
    const dia = String(fecha.getDate()).padStart(2, "0");
    const mes = String(fecha.getMonth() + 1).padStart(2, "0");
    const año = fecha.getFullYear();
    const fechaFormateada = `${dia}/${mes}/${año}`;

    return (
      <div className="bg-white shadow-md rounded-lg p-4 max-w-2xl mx-auto text-negro">
        <h3 className="text-xl font-bold mb-4 text-center">
          {tipo === "próximo" ? "Próximo Partido" : "Último Partido"}
        </h3>

        {/* Línea competición */}
        <div className="text-center text-sm text-gray-600 space-y-1 mb-2">
          <p className="">{partido.nombre_competicion}</p>
        </div>

        {/* Línea de jornada */}
        <div className="text-center text-sm text-gray-600 space-y-1 mb-2">
          <p>Jornada {partido.jornada}</p>
        </div>

        {/* Línea de equipos y resultado/VS */}
        <div className="flex justify-between items-center text-white font-semibold mb-2">
          {/* Equipo Local */}
          <div className="w-1/3 text-left text-black">{partido.local}</div>

          {/* Resultado o VS */}
          <div className="w-1/3 text-center text-black text-2xl font-bold">
            {tipo === "último"
              ? `${partido.resultado_local} - ${partido.resultado_visitante}`
              : "vs"}
          </div>

          {/* Equipo Visitante */}
          <div className="w-1/3 text-right text-black">{partido.visitante}</div>
        </div>

        {/* Línea fecha */}
        <div className="text-center text-sm text-gray-600 space-y-1">
          <p>{fechaFormateada}</p>
        </div>

        {/* Línea hora */}
        <div className="text-center text-sm text-gray-600 space-y-1">
          {tipo === "próximo" &&
            partido.hora?.match(/^\d{2}:\d{2}:\d{2}$/) && <p>{partido.hora.slice(0, 5)}</p>}
        </div>
      </div>
    );
  };

  return (
    <section className="bg-celeste text-black px-4 py-8 text-blanco rounded-[1rem] font-bold font-poetsen">
      <h2 className="text-2xl font-bold mb-6 text-center">Partidos</h2>
      {/* Botones categoría */}
      <div className="flex justify-center gap-4 mb-6">
        {(["Senior", "Femenino", "Juvenil"] as const).map((cat) => (
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

      <div className="flex flex-col md:flex-row gap-6 justify-between items-stretch max-w-4xl mx-auto">
        <div className="md:w-1/2 bg-blanco rounded-[1rem]">{renderPartido(ultimo, "último")}</div>
        <div className="md:w-1/2 bg-blanco rounded-[1rem]">{renderPartido(proximo, "próximo")}</div>
      </div>
    </section>
  );
}

