import { Link } from "react-router-dom";
import { useState, useEffect } from "react";

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

const FILAS_POR_PAGINA = 1;
const COLUMNAS = 3;
const IMAGENES_POR_PAGINA = FILAS_POR_PAGINA * COLUMNAS;

type ContenidoItem = {
  id: number;
  tipo: "texto" | "imagen";
  contenido: string; // texto o url imagen
  lugar: string;
  orden: number;
};

export default function Historia() {
  const width = useWindowWidth();
  const [contenido, setContenido] = useState<ContenidoItem[]>([]);
  const [paginaActual, setPaginaActual] = useState(1);

  useEffect(() => {
    async function fetchContenido() {
      try {
        const res = await fetch("https://aplicacion-web-m5oa.onrender.com/contenido/?lugar=Historia");
        if (!res.ok) throw new Error("Error al cargar contenido");
        const data: ContenidoItem[] = await res.json();
        setContenido(data.sort((a, b) => a.orden - b.orden));
      } catch (error) {
        console.error(error);
      }
    }
    fetchContenido();
  }, []);

  if (width === null) return null;

  const textos = contenido.filter((item) => item.tipo === "texto");
  const imagenes = contenido.filter((item) => item.tipo === "imagen");

  const totalPaginas = Math.ceil(imagenes.length / IMAGENES_POR_PAGINA);

  const imagenesPagina = imagenes.slice(
    (paginaActual - 1) * IMAGENES_POR_PAGINA,
    paginaActual * IMAGENES_POR_PAGINA
  );

  const cambiarPagina = (direccion: "anterior" | "siguiente") => {
    setPaginaActual((prev) => {
      if (direccion === "anterior" && prev > 1) return prev - 1;
      if (direccion === "siguiente" && prev < totalPaginas) return prev + 1;
      return prev;
    });
  };

  return (
    <main className="max-w-screen-xl mx-auto p-6 font-sans">
      <section className="bg-celeste text-blanco px-4 py-8 rounded-[1rem] font-bold font-poetsen">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">
          Historia del Club
        </h1>

        {/* Texto dinámico */}
        {textos.map((item) => (
          <p
            key={item.id}
          >
            <pre className="whitespace-pre-wrap break-words overflow-hidden text-negro_texto font-poetsen">
              	{item.contenido}
              </pre>
          </p>
        ))}
        
         <div className="flex justify-center items-center mb-6">	
  <Link
    to="/club-antiguo"
    className="no-underline px-6 py-2 rounded-full font-bold border-2 transition-all bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
  >
    Más Historia
  </Link>     
</div>

</section>
        <section className="bg-blanco text-blanco px-4 py-8 rounded-[1rem] font-bold font-poetsen">
        </section>
        <section className="bg-celeste text-blanco px-4 py-8 rounded-[1rem] font-bold font-poetsen">

        {/* Galería dinámica */}
        <div className="mt-12">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
            Galería
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {imagenesPagina.map((item) => (
              <img
                key={item.id}
                src={item.contenido}
                alt={``}
                className="w-full h-48 object-cover rounded-xl shadow-md"
              />
            ))}
          </div>

          {/* Paginación */}
          {totalPaginas > 1 && (
            <div className="flex justify-center items-center gap-6 mt-8">
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
        </div>
      </section>
    </main>
  );
}

