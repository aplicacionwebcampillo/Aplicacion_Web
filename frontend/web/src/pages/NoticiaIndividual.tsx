import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";


interface Noticia {
  titular: string;
  imagen: string;
  contenido: string;
  categoria: string;
  dni_administrador: string;
}

export default function NoticiaIndividual() {
  const { titular } = useParams<{ titular: string }>();
  const [noticia, setNoticia] = useState<Noticia | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!titular) return;

    setLoading(true);
    fetch(`https://aplicacion-web-m5oa.onrender.com/noticias/${encodeURIComponent(titular)}`)
      .then(res => {
        if (!res.ok) throw new Error("Noticia no encontrada");
        return res.json();
      })
      .then(data => {
        setNoticia(data);
        setError(null);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [titular]);

  if (loading) return <p>Cargando noticia...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!noticia) return <p>No se encontró la noticia.</p>;

  return (
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto m-[0%] p-[2%] font-sans">
     <section className="text-black px-4 py-8 text-negro rounded-[1rem] font-bold font-poetsen">
      <Link to="/noticias" className="text-negro no-underline font-semibold mb-4 inline-block hover:text-azul">
        ← Volver al menú de noticias
      </Link>
      
      <div className="bg-celeste text-black px-4 py-8 text-negro rounded-[1rem] font-bold font-poetsen">
      <h1 className="text-3xl font-bold mb-4 text-center font-poetsen">{noticia.titular}</h1>
      <div className="flex justify-center">
        <img
          src={noticia.imagen || "/images/PorDefecto.png"}
          alt={noticia.titular}
          className="h-[20rem] md:h-[30rem] w-auto object-cover"
        />
      </div>
      <h1></h1>
      <div className="text-justify flex justify-center text-negro_texto font-poetsen" dangerouslySetInnerHTML={{ __html: noticia.contenido }} />
      </div>
     </section>
    </main>
  );
}

