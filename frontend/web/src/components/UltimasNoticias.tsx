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

// Ver el mismo criterio en components/Noticias.tsx: el modelo de Noticia no
// tiene columna de fecha, así que la extraemos del titular cuando la trae
// (formato "Título (DD/MM/AAAA)", usado por el importador de Instagram).
function claveOrden(noticia: Noticia): number {
  const match = noticia.titular.match(/\((\d{2})\/(\d{2})\/(\d{4})\)\s*$/);
  if (match) {
    const [, dd, mm, yyyy] = match;
    return new Date(Number(yyyy), Number(mm) - 1, Number(dd)).getTime();
  }
  return Number(noticia.id_noticia || 0) - 1e15;
}

export default function UltimasNoticias() {
  const [noticias, setNoticias] = useState<Noticia[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://aplicacion-web-m5oa.onrender.com/noticias/?skip=0&limit=100")
      .then((res) => res.json())
      .then((data) => {
        setNoticias(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error cargando noticias:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="text-center text-gray-500">Cargando noticias...</p>;
  }

  return (
<section className="bg-celeste px-4 py-8 text-blanco rounded-[1rem] font-poetsen">
  <h2 className="text-2xl font-bold mb-6 text-center font-bold">Últimas Noticias</h2>

  <div className="flex justify-center">
   <div className="flex gap-4 overflow-x-auto pb-2 px-2 max-w-full text-center">
  {[...noticias].sort((a, b) => claveOrden(b) - claveOrden(a)).slice(0, 3).map((noticia, index) => (
    <Link
      key={index}
      to={`/noticias/id/${noticia.id_noticia}`}
      className="min-w-[19rem] min-h-[23rem] md:max-w-[33.33%] bg-blanco text-black shadow rounded-[1rem] p-4 flex-shrink-0 flex flex-col items-center hover:shadow-lg transition-shadow duration-300 no-underline  hover:border-3 hover:border-azul"
    >
      <div className="h-40 w-full bg-gray-300 rounded mb-2 overflow-hidden flex justify-center items-center">
        <img
          src={noticia.imagen || "/images/PorDefecto.png"}
          alt={noticia.titular}
          className="h-[15rem] w-auto object-cover"
        />
      </div>
      <div className="p-4 text-center w-full">
        <h3 className="text-lg font-semibold mb-1 text-negro">{noticia.titular}</h3>
      </div>
    </Link>
  ))}
</div>

  </div>
</section>


  );
}

