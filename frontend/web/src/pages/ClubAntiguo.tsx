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

const ClubAntiguo = () => {
 // Galería: reemplaza las rutas por las de tus imágenes reales
  const images = [
    "/images/ClubAntiguo1.jpeg",
    "/images/ClubAntiguo2.jpeg",
    "/images/ClubAntiguo3.jpeg",
    "/images/ClubAntiguo4.jpg",
    "/images/ClubAntiguo5.jpg",
    "/images/ClubAntiguo6.jpg",
    "/images/ClubAntiguo7.jpg",
    "/images/ClubAntiguo8.jpg",
    "/images/ClubAntiguo9.jpg",
    "/images/ClubAntiguo10.jpg",
    "/images/ClubAntiguo11.jpg",
    "/images/ClubAntiguo12.jpg",
  ];

  const [paginaActual, setPaginaActual] = useState(1);

  const width = useWindowWidth();
  
  const totalPaginas = Math.ceil(images.length / IMAGENES_POR_PAGINA);

  // Recortar images de la página actual
  //const imagesPagina = images.slice(
    //(paginaActual - 1) * IMAGENES_POR_PAGINA,
   // paginaActual * IMAGENES_POR_PAGINA
  //);
  

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
      <section className="bg-celeste text-negro_texto px-4 py-8  rounded-[1rem] font-bold font-poetsen">
        <h1>Torreblascopedro C.F.</h1>
        <p>
          El Torreblascopedro Club de Fútbol fue fundado en 1984 y participó en competiciones regionales hasta 1988. Durante su existencia, compitió en la Segunda Regional de Jaén, obteniendo su mejor posición en la temporada 1987-88, donde finalizó en el 8º lugar. El club tenía su sede en Torreblascopedro, Jaén. 
        </p>
        
        <div className="overflow-x-auto">
        <table className="min-w-full table-auto border-[0.2rem] border-azul bg-blanco text-negro_texto rounded-[1rem]">
          <thead className="text-negro">
            <tr>
              <th>Temporada</th>
              <th>Federación</th>
              <th>Competición</th>
              <th>Pos</th>
              <th>Pts</th>
              <th>PJ</th>
              <th>PG</th>
              <th>PE</th>
              <th>PP</th>
              <th>GF</th>
              <th>GC</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1987-88</td>
              <td>Andaluza</td>
              <td><a 
    href="https://www.futbol-regional.es/competicion.php?1987-88_AND_3_Segunda_Regional_-_Jaen-02&com=24161" 
    target="_blank" 
    rel="noopener noreferrer"
    className="no-underline text-negro_texto hover:text-azul"
  >
    3. Segunda Regional - Jaén-02
  </a></td>
              <td>8º</td>
              <td>7</td>
              <td>15</td>
              <td>3</td>
              <td>1</td>
              <td>11</td>
              <td>23</td>
              <td>48</td>
            </tr>
            <tr>
              <td>1986-87</td>
              <td colSpan={8} className="text-center">Datos no disponibles</td>
            </tr>
            <tr>
              <td>1985-86</td>
              <td>Andaluza</td>
              <td><a 
    href="https://www.futbol-regional.es/competicion.php?1985-86_AND_3_Segunda_Regional_-_Jaen-02&com=24168" 
    target="_blank" 
    rel="noopener noreferrer"
    className="no-underline text-negro_texto hover:text-azul"
  >
    3. Segunda Regional - Jaén-02
  </a></td>
              <td>10º</td>
              <td>8</td>
              <td>18</td>
              <td>4</td>
              <td>4</td>
              <td>10</td>
              <td>22</td>
              <td>28</td>
            </tr>
            <tr>
              <td>1984-85</td>
              <td colSpan={8} className="text-center">Datos desconocidos</td>
            </tr>
          </tbody>
        </table>
        </div>
        
      </section>

      <section className="bg-celeste text-negro_texto px-4 py-8  rounded-[1rem] font-bold font-poetsen">
        <h1>Campillo del Río C.F.</h1>
        <p>
          El Campillo del Río Club de Fútbol se estableció en 2004 y compitió hasta 2006. Durante su corta trayectoria, participó en la Primera Provincial de Jaén, alcanzando su mejor clasificación en la temporada 2005-06 con un 6º puesto. El club estaba ubicado en Campillo del Río, una pedanía de Torreblascopedro, Jaén. 
        </p>
        <div className="overflow-x-auto">
        <table className="min-w-full table-auto border-[0.2rem] border-azul bg-blanco text-negro_texto rounded-[1rem]">
          <thead className="text-negro">
            <tr>
              <th>Temporada</th>
              <th>Federación</th>
              <th>Competición</th>
              <th>Pos</th>
              <th>Pts</th>
              <th>PJ</th>
              <th>PG</th>
              <th>PE</th>
              <th>PP</th>
              <th>GF</th>
              <th>GC</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>2005-06</td>
              <td>Andaluza</td>
              <td><a 
    href="https://www.futbol-regional.es/competicion.php?2005-06_AND_3_Primera_Provincial_-_Jaen-02&com=24031" 
    target="_blank" 
    rel="noopener noreferrer"
    className="no-underline text-negro_texto hover:text-azul"
  >
    3. Primera Provincial - Jaén-02
  </a></td>
              <td>6º</td>
              <td>21</td>
              <td>15</td>
              <td>7</td>
              <td>0</td>
              <td>8</td>
              <td>20</td>
              <td>17</td>
            </tr>
            <tr>
              <td>2004-05</td>
              <td>Andaluza</td>
              <td><a 
    href="https://www.futbol-regional.es/competicion.php?2004-05_AND_3_Primera_Provincial_-_Jaen&com=24035" 
    target="_blank" 
    rel="noopener noreferrer"
    className="no-underline text-negro_texto hover:text-azul"
  >
    3. Primera Provincial - Jaén
  </a></td>
              <td>13º</td>
              <td>18</td>
              <td>26</td>
              <td>5</td>
              <td>3</td>
              <td>18</td>
              <td>33</td>
              <td>60</td>
            </tr>
          </tbody>
        </table>
        </div>
      </section>
      
      {/* Galería */}
      <section className="bg-celeste text-negro_texto px-4 py-8  rounded-[1rem] font-bold font-poetsen">
        <div className="mt-16">
          <h3 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
            Galería Histórica
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
};

export default ClubAntiguo;

