import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface Noticia {
  id_noticia: string;
  titular: string;
  imagen: string;
  contenido: string;
  categoria: string;
  dni_administrador: string;
}

const CATEGORIAS = [
  "Senior Masculino",
  "Senior Femenino",
  "Cantera",
  "Noticias del Club",
  "Comunicados Oficiales",
  "Actividades Sociales",
];


// El modelo de Noticia no tiene columna de fecha; las noticias importadas
// de Instagram llevan la fecha de publicación al final del titular, p.ej.
// "Título (20/07/2026)". La extraemos para poder ordenar por fecha real.
// Las noticias sin fecha en el título (creadas a mano) se consideran las
// más antiguas de todas a efectos de orden.
function claveOrden(noticia: Noticia): number {
  const match = noticia.titular.match(/\((\d{2})\/(\d{2})\/(\d{4})\)\s*$/);
  if (match) {
    const [, dd, mm, yyyy] = match;
    return new Date(Number(yyyy), Number(mm) - 1, Number(dd)).getTime();
  }
  return Number(noticia.id_noticia || 0) - 1e15;
}

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

const FILAS_POR_PAGINA = 3;
const COLUMNAS = 3;
const NOTICIAS_POR_PAGINA = FILAS_POR_PAGINA * COLUMNAS;

export default function NoticiasMain() {
  const [noticias, setNoticias] = useState<Noticia[]>([]);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState<string | null>(null);
  const [paginaActual, setPaginaActual] = useState(1);

  useEffect(() => {
    fetch("https://aplicacion-web-m5oa.onrender.com/noticias/?skip=0&limit=100")
      .then((res) => res.json())
      .then((data: Noticia[]) => {
        setNoticias(data);
      })
      .catch((err) => console.error("Error al cargar noticias:", err));
  }, []);

  const noticiasFiltradas = categoriaSeleccionada
    ? noticias.filter((n) => n.categoria === categoriaSeleccionada)
    : noticias;

  const handleCategoriaClick = (cat: string) => {
    setCategoriaSeleccionada(cat === categoriaSeleccionada ? null : cat);
    setPaginaActual(1);
  };
  
  const width = useWindowWidth();
  
  const noticiasOrdenadas = [...noticiasFiltradas].sort(
    (a, b) => claveOrden(b) - claveOrden(a)
  );


  const totalPaginas = Math.ceil(noticiasOrdenadas.length / NOTICIAS_POR_PAGINA);

  // Recortar noticias de la página actual
  const noticiasPagina = noticiasOrdenadas.slice(
    (paginaActual - 1) * NOTICIAS_POR_PAGINA,
    paginaActual * NOTICIAS_POR_PAGINA
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
  }, [categoriaSeleccionada]);

  if (width === null) return null;
  
  return (
    <section className="bg-celeste text-black px-4 py-8 text-blanco rounded-[1rem] font-bold font-poetsen">
      <h2 className="text-2xl font-bold mb-4 text-center text-blanco">Noticias</h2>
      {/* Botones Categoria */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
      <button
        onClick={() => {
          setCategoriaSeleccionada(null);
          setPaginaActual(1);
        }}
        className={`px-4 py-2 rounded-full border-2 font-semibold transition-all ${
          categoriaSeleccionada === null
            ? "bg-azul text-blanco border-azul"
            : "bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        }`}
      >
        Todas
      </button>

      {CATEGORIAS.map((cat) => (
        <button
          key={cat}
          onClick={() => handleCategoriaClick(cat)}
          className={`px-4 py-2 rounded-full border-2 font-semibold transition-all ${
            categoriaSeleccionada === cat
              ? "bg-azul text-blanco border-azul"
              : "bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          }`}
        >
          {cat}
        </button>
      ))}
    </div>

    {/* Tarjetas de noticias */}
    <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
  {noticiasPagina.map((noticia, idx) => (
    <Link
      key={idx}
      to={`/noticias/id/${noticia.id_noticia}`}
      className="no-underline min-w-[19rem] min-h-[23rem] bg-white text-black shadow rounded-lg p-4 flex-shrink-0 bg-blanco rounded-[1rem] flex flex-col items-center hover:shadow-lg transition-shadow duration-300 hover:border-2 hover:border-azul"
    >
      <div className="h-40 w-full bg-gray-300 rounded mb-2 overflow-hidden flex justify-center items-center">
        <img
          src={noticia.imagen || "/images/PorDefecto.png"}
          alt={noticia.titular}
          className="h-[15rem] w-auto object-cover rounded-[1rem]"
        />
      </div>
      <div className="p-4 text-center w-full">
        <h3 className="text-lg font-semibold mb-1 text-negro">{noticia.titular}</h3>
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

