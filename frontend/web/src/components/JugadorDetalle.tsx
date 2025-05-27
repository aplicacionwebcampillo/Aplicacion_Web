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
    fetch(`http://localhost:8000/jugadores/${id}`)
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

      <div className="flex flex-col md:flex-row gap-6 items-center bg-celeste text-black px-4 py-8 text-negro rounded-[1rem] font-bold font-poetsen">
        <img
          src={jugador.foto || "/images/PorDefecto.png"}
          alt={jugador.nombre}
          className="w-full h-auto object-cover rounded-lg shadow-md"
        />

        <div className="flex flex-col gap-3">
          <h1 className="text-3xl font-bold text-negro">{jugador.nombre}</h1>
          <p>
  <strong>Posición:</strong>{" "}
  <span className="text-negro_texto">{jugador.posicion}</span>
</p>
<p>
  <strong>Dorsal:</strong>{" "}
  <span className="text-negro_texto">{jugador.dorsal}</span>
</p>
<p>
  <strong>Fecha de nacimiento:</strong>{" "}
  <span className="text-negro_texto">
    {new Date(jugador.fecha_nacimiento).toLocaleDateString()}
  </span>
</p>
<p className="mt-4 text-negro_texto text-justify">{jugador.biografia}</p>

        </div>
      </div>
    </section>
  );
}

