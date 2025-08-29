import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

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

export default function JugadorDetalle() {
  const { id } = useParams<{ id: string }>();
  const [jugador, setJugador] = useState<Jugador | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    setLoading(true);
    fetch(`https://aplicacion-web-m5oa.onrender.com/jugadores/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error("Jugador no encontrado");
        return res.json();
      })
      .then((data: Jugador) => {
        setJugador(data);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p>Cargando jugador...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!jugador) return <p>No se encontró el jugador.</p>;

  return (
    <section className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md font-poetsen">
      <Link to="/plantilla" className="text-negro no-underline font-semibold mb-4 inline-block hover:text-azul">
        ← Volver a la plantilla
      </Link>

      <div className="bg-celeste text-black px-4 py-8 text-negro rounded-[1rem] font-bold font-poetsen">
      <div className="flex justify-center"> 
      	<img 
      	  src={jugador.foto || "/images/PorDefecto.png"} 
      	  alt={jugador.nombre} 
      	  className="h-[20rem] md:h-[30rem] w-auto object-cover rounded-lg shadow-md" 
      	/> 
      </div>
      	
      	<div className="flex justify-center"> 
      	<div className="flex flex-col gap-3">
      	  <h1 className="text-3xl font-bold mb-4 text-center font-poetsen">{jugador.nombre}</h1> 
      	  <p> 
      	    <strong>Posición:</strong>{" "} 
      	    <span className="text-negro_texto">{jugador.posicion}</span> 
      	    </p> 
      	      {jugador.dorsal !== 0 && ( 
      	        <p> 
      	          <strong>Dorsal:</strong>{" "} 
      	          <span className="text-negro_texto">{jugador.dorsal}</span> 
      	        </p> 
      	      )} 
      	      <p> 
      	        <strong>Fecha de nacimiento:</strong>{" "} 
      	        <span className="text-negro_texto"> {new Date(jugador.fecha_nacimiento).toLocaleDateString()} </span> 
      	      </p> 
      	      <p className="text-justify flex justify-center text-negro_texto font-poetsen w-[40rem] md:w-[50rem] h-auto">{jugador.biografia}</p> 
      	</div> 
      	</div> 
      </div>

    </section>
  );
}

