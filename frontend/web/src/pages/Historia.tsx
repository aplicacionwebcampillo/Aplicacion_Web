import React, { useState, useEffect } from "react";
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

const FILAS_POR_PAGINA = 1;
const COLUMNAS = 3;
const IMAGENES_POR_PAGINA = FILAS_POR_PAGINA * COLUMNAS;

export default function Historia() {
  // Galería: reemplaza las rutas por las de tus imágenes reales
  const images = [
    "/images/PrimeraDirectiva.jpeg",
    "/images/PrimeraDirectiva2.jpeg",
    "/images/ActualDirectiva.jpeg",
    "/images/PresentacionAño1.jpeg",
    "/images/PresentacionAño2.jpeg",
    "/images/PresentacionAño3.jpeg",
    "/images/PresentacionAño4.jpeg",
    "/images/Equipo0.jpg",
    "/images/Equipo.jpg",
    "/images/Equipo2.jpg",
    "/images/Equipo3.jpg",
  ];

  const [paginaActual, setPaginaActual] = useState(1);

  const width = useWindowWidth();
  
  const totalPaginas = Math.ceil(images.length / IMAGENES_POR_PAGINA);

  // Recortar images de la página actual
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
  
  const startIndex = (paginaActual - 1) * IMAGENES_POR_PAGINA;
  const endIndex = paginaActual * IMAGENES_POR_PAGINA;
  const paginatedImages = images.slice(startIndex, endIndex);

  
  return (
   
  
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto m-[0%] p-[2%] font-sans">
     <section className="bg-celeste text-blanco px-4 py-8  rounded-[1rem] font-bold font-poetsen">
     	<h2 className="text-4xl font-bold text-center mb-8">
        Historia del Club
      </h2>
      <div className="space-y-6 text-blancotext-base leading-relaxed text-negro_texto">
        <p>
          En el corazón de la provincia de Jaén, en la pequeña pedanía de <strong>Campillo del Río</strong>, perteneciente al municipio de Torreblascopedro y con apenas 625 habitantes, el fútbol ha vuelto a cobrar vida. Tras 17 años sin un equipo federado, un grupo de amigos decidió reunirse en enero de 2022, durante una cena marcada por la ilusión del nuevo campo de fútbol, y comenzó a gestarse un sueño: devolver el fútbol al pueblo.
        </p>
        <p>
          Los primeros en hablar del proyecto fueron <strong>Francisco Muñoz</strong>, <strong>Jairo Ortiz</strong>, <strong>Luis Carlos Martínez</strong> y <strong>María José Moreno</strong>, quien tomó la iniciativa de contactar con el Registro de Entidades Deportivas de Andalucía y la Federación Andaluza de Fútbol para conocer los pasos necesarios para la fundación del club. Pronto se sumó a la idea <strong>Alejandro Martínez</strong>, actual capitán del equipo, completando así los cinco miembros iniciales de la junta directiva.
        </p>
        <p>
          Con este grupo inicial se solicitó una reunión con el alcalde <strong>Juan María Ruiz</strong> y la concejala de deportes <strong>Noelia Muñoz</strong>, quienes brindaron su apoyo al proyecto.
        </p>
        <p>
          El <strong>diseño del escudo</strong> corrió a cargo del arquitecto local <strong>Javier Civantos</strong>. También se unió a la junta <strong>Luisa María Martínez</strong>, quien continúa colaborando activamente.
        </p>
        <p>
          El banquillo quedó bajo la dirección de <strong>Luis Carlos Ramos</strong>, que en sus inicios contó con la ayuda de <strong>Manolo Díaz</strong>, primer entrenador provisional.
        </p>
        <p>
          El club no habría sido posible sin el apoyo de muchas personas: <strong>Miguel Moreno</strong> con el equipo audiovisual, <strong>Raquel Moreno</strong> con redes sociales, <strong>Francisco Macías</strong>, <strong>Iván Fernández</strong>, <strong>Lucas López</strong>, <strong>María Fernández</strong> y <strong>Victoriano Civantos</strong>, quien grabó todos los partidos.
        </p>
        <p>
          También nació un equipo <strong>femenino</strong>, surgido de una liga de fútbol 7 con <strong>Antonio Miguel Civantos</strong> al mando, y con entrenadores como <strong>Manolo Díaz</strong> y <strong>Manuel Fernández</strong>. Además, por primera vez, se creó una <strong>cantera de niños</strong>, liderada por <strong>Francisco Manuel Martínez Villodres</strong> y <strong>Miguel Serrano</strong>, con el apoyo del Ayuntamiento.
        </p>
        <p>
          En la temporada 2024/2025, la directiva está formada por <strong>María José Moreno</strong> (Presidenta), <strong>Luisa María Martínez</strong>, <strong>Alejandro Martínez</strong>, <strong>José Luis Molina</strong>, <strong>Francisco José Macías</strong> (Marketing) y <strong>Jairo Ortiz</strong>, quien se despide esta temporada.
        </p>
        <p>
          El <strong>C.D. Campillo del Río C.F.</strong> no es solo un equipo. Es el reflejo de un pueblo que se niega a dejar morir su pasión por el fútbol. Un proyecto colectivo que ha resucitado la ilusión, el compañerismo y el orgullo local. Y así, desde este rincón de Jaén, comienza a escribirse una nueva historia.
        </p>
      </div>
      
      <div className="flex justify-center items-center mb-6">	
  <Link
    to="/club-antiguo"
    className="no-underline px-6 py-2 rounded-full font-bold border-2 transition-all bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
  >
    Más Historia
  </Link>     
</div>

      
      {/* Galería */}
        <div className="mt-16">
          <h3 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
            Galería
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {paginatedImages.map((src, index) => (
              <img
                key={index}
                src={src}
                alt={`Imagen ${startIndex + index + 1}`}
                className="w-full h-64 object-cover rounded-xl shadow-md"
              />
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
