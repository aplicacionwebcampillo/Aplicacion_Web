import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

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

interface Jugador {
  id_jugador: number;
  nombre: string;
  posicion: string;
  fecha_nacimiento: string;
  foto: string;
  biografia: string;
  dorsal: number;
  id_equipo: number;
}

const CATEGORIAS_EQUIPO = [
  { id: 1, nombre: "Senior" },
  { id: 2, nombre: "Femenino" },
  { id: 3, nombre: "Juvenil" },
];

const FILAS_POR_PAGINA = 3;
const COLUMNAS = 3;
const JUGADORES_POR_PAGINA = FILAS_POR_PAGINA * COLUMNAS;

export default function Plantilla() {
  const [jugadores, setJugadores] = useState<Jugador[]>([]);
  const [equipoSeleccionado, setEquipoSeleccionado] = useState<number | null>(null);
  const [paginaActual, setPaginaActual] = useState(1);

  const width = useWindowWidth();

  useEffect(() => {
    fetch("https://aplicacion-web-m5oa.onrender.com/jugadores/?skip=0&limit=100")
      .then((res) => res.json())
      .then((data: Jugador[]) => setJugadores(data))
      .catch((err) => console.error("Error al cargar jugadores:", err));
  }, []);

  // Filtrar según equipo seleccionado
  const jugadoresFiltrados = equipoSeleccionado
    ? jugadores.filter((j) => j.id_equipo === equipoSeleccionado)
    : jugadores;
    
  const jugadoresOrdenados = [...jugadoresFiltrados].sort(
  (a, b) => Number(a.dorsal) - Number(b.dorsal)
);


  const totalPaginas = Math.ceil(jugadoresOrdenados.length / JUGADORES_POR_PAGINA);

  // Recortar jugadores de la página actual
  const jugadoresPagina = jugadoresOrdenados.slice(
    (paginaActual - 1) * JUGADORES_POR_PAGINA,
    paginaActual * JUGADORES_POR_PAGINA
  );

  const cambiarPagina = (direccion: "anterior" | "siguiente") => {
    setPaginaActual((prev) => {
      if (direccion === "anterior" && prev > 1) return prev - 1;
      if (direccion === "siguiente" && prev < totalPaginas) return prev + 1;
      return prev;
    });
  };

  // Resetear página cuando cambia el filtro
  useEffect(() => {
    setPaginaActual(1);
  }, [equipoSeleccionado]);

  if (width === null) return null;

  return (
    <section className="bg-celeste text-black px-4 py-8 rounded-[1rem] font-bold font-poetsen">
      <h2 className="text-2xl font-bold mb-4 text-center text-blanco">Plantilla</h2>
      {/* Botones de categoría */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        <button
          onClick={() => setEquipoSeleccionado(null)}
          className={`px-4 py-2 rounded-full border-2 font-semibold transition-all ${
            equipoSeleccionado === null
              ? "bg-azul text-blanco border-azul"
              : "bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          }`}
        >
          Todos
        </button>

        {CATEGORIAS_EQUIPO.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setEquipoSeleccionado(cat.id)}
            className={`px-4 py-2 rounded-full border-2 font-semibold transition-all ${
              equipoSeleccionado === cat.id
                ? "bg-azul text-blanco border-azul"
                : "bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            }`}
          >
            {cat.nombre}
          </button>
        ))}
      </div>

      {/* Tarjetas de jugadores */}
      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
  {jugadoresPagina.map((jugador) => (
    <Link
      to={`/jugadores/${jugador.nombre}`}
      key={jugador.id_jugador}
      className="min-w-[19rem] bg-white text-black shadow rounded-lg p-4 flex-shrink-0 bg-blanco rounded-[1rem] flex flex-col items-center hover:shadow-lg transition-shadow duration-300 no-underline hover:border-3 hover:border-azul"
    >
      <div className="h-40 w-full bg-gray-200 rounded mb-2 overflow-hidden flex justify-center items-center">
        <img
          src={jugador.foto || "/images/PorDefecto.png"}
          alt={jugador.nombre}
          className="h-[15rem] w-auto object-cover"
        />
      </div>
      <div className="p-4 text-center w-full">
        <h3 className="text-lg font-semibold mb-1 text-negro">{jugador.nombre}</h3>
      </div>
    </Link>
  ))}
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
          <span className="text-lg font-bold">{paginaActual} / {totalPaginas}</span>
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

