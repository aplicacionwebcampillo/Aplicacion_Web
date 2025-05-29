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

export default function Instalaciones() {
  // Rutas de imágenes de las instalaciones
  const images = [
    "/images/PorDefecto.png",
    "/images/PorDefecto.png",
    "/images/PorDefecto.png",
    "/images/PorDefecto.png",
    "/images/PorDefecto.png",
    "/images/PorDefecto.png",
    "/images/PorDefecto.png",
    "/images/PorDefecto.png",
    
  ];

  const [paginaActual, setPaginaActual] = useState(1);

  const width = useWindowWidth();

  const totalPaginas = Math.ceil(images.length / IMAGENES_POR_PAGINA);

  const imagesPagina = images.slice(
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

  if (width === null) return null;

  return (
    <main className="max-w-screen-xl mx-auto p-6 font-sans">
      <section className="bg-celeste text-blanco px-4 py-8  rounded-[1rem] font-bold font-poetsen">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">
          Instalaciones Deportivas
        </h1>

        <p className="mb-6 text-gray-700 leading-relaxed text-justify">
          El <strong>Campo Municipal de Campillo del Río</strong> es el epicentro del fútbol en nuestra localidad. Tras años sin fútbol federado, este espacio ha sido reformado y acondicionado para recibir tanto al equipo sénior como a los equipos femeninos y juveniles que representan con orgullo a nuestro pueblo.
        </p>

        <p className="mb-6 text-gray-700 leading-relaxed text-justify">
          Gracias al apoyo del Ayuntamiento y la inversión realizada, las
          instalaciones cuentan con césped de alta calidad (Dimensiones: 100x58m), gradas para
          espectadores (Aforo permitido: 270 personas) y vestuarios modernos que cumplen con los requisitos
          deportivos.
        </p>

        {/* Galería */}
        <div className="mt-12">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
            Galería de Instalaciones
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {imagesPagina.map((src, index) => (
              <img
                key={index}
                src={src}
                alt={`Instalación ${index + 1 + (paginaActual - 1) * IMAGENES_POR_PAGINA}`}
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

