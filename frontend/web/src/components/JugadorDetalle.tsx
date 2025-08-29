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

      <div className="flex justify-center px-4">
  <div className="flex flex-col gap-4 max-w-3xl w-full">
    {/* Nombre */}
    <h1 className="text-3xl font-bold mb-4 text-center font-poetsen">
      {jugador.nombre}
    </h1>

    {/* Posición */}
    <p>
      <strong>Posición:</strong>{" "}
      <span className="text-negro_texto">{jugador.posicion}</span>
    </p>

    {/* Dorsal */}
    {jugador.dorsal !== 0 && (
      <p>
        <strong>Dorsal:</strong>{" "}
        <span className="text-negro_texto">{jugador.dorsal}</span>
      </p>
    )}

    {/* Fecha de nacimiento */}
    <p>
      <strong>Fecha de nacimiento:</strong>{" "}
      <span className="text-negro_texto">
        {new Date(jugador.fecha_nacimiento).toLocaleDateString()}
      </span>
    </p>

    {/* Biografía */}
    <p className="text-justify text-negro_texto font-poetsen leading-relaxed">
      {jugador.biografia}
    </p>
  </div>
</div>

    </section>
  );
}

