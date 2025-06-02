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
  {noticias.slice(-3).reverse().map((noticia, index) => (
    <Link
      key={index}
      to={`/noticias/${encodeURIComponent(noticia.titular)}`}
      className="min-w-[19rem] min-h-[23rem] md:max-w-[33.33%] bg-blanco text-black shadow rounded-[1rem] p-4 flex-shrink-0 flex flex-col items-center hover:shadow-lg transition-shadow duration-300 no-underline  hover:border-3 hover:border-azul"
    >
      <div className="h-40 w-full bg-gray-300 rounded mb-2 overflow-hidden flex justify-center items-center">
        <img
          src={noticia.imagen || "/images/PorDefecto.png"}
          alt={noticia.titular}
          className="h-[15rem] w-auto object-cover"
        />
      </div>
      <h3 className="text-lg font-semibold mb-1 text-negro">{noticia.titular}</h3>
    </Link>
  ))}
</div>

  </div>
</section>


  );
}

