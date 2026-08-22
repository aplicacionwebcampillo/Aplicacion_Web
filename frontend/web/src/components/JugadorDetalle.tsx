import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

interface Jugador {
  id_jugador: number;
  nombre: string;
  posicion: string;
  fecha_nacimiento: string | null;
  foto: string;
  biografia: string;
  dorsal: number;
  id_equipo: number;
  nombre_corto: string | null;
  nombre_completo: string | null;
  estado_fichaje: string | null;
  partidos_jugados: number;
  partidos_titular: number;
  goles: number;
  tarjetas_amarillas: number;
  tarjetas_rojas: number;
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

    <div className="flex flex-col md:flex-row gap-6 items-center bg-celeste text-black px-4 py-8 text-negro rounded-[1rem] font-bold font-poetsen">
  <img
    src={jugador.foto || "/images/PorDefecto.png"}
    alt={jugador.nombre}
    className="max-h-[20rem] md:max-h-[30rem] w-auto max-w-full object-contain rounded-lg shadow-md"
  />

      <div className="flex justify-center px-4">
  <div className="flex flex-col gap-4 max-w-3xl w-full md:w-[50%]">
    {/* Nombre */}
    <h1 className="text-3xl font-bold mb-1 text-center font-poetsen">
      {jugador.nombre_completo || jugador.nombre}
    </h1>
    {jugador.nombre_corto && jugador.nombre_corto !== jugador.nombre_completo && (
      <p className="text-center text-negro_texto -mt-3">"{jugador.nombre_corto}"</p>
    )}

    {/* Estado de fichaje/renovación */}
    {jugador.estado_fichaje && (
      <p className="text-center">
        <span className="inline-block bg-azul text-white text-sm px-3 py-1 rounded-full">
          {jugador.estado_fichaje}
        </span>
      </p>
    )}

    {/* Posición */}
    <p>
      <strong>Posición:</strong>{" "}
      <span className="text-negro_texto">{jugador.posicion}</span>
    </p>

    {/* Dorsal */}
    {![0, 26, 27, 28].includes(jugador.dorsal) && (
  <p>
    <strong>Dorsal:</strong>{" "}
    <span className="text-negro_texto">{jugador.dorsal}</span>
  </p>
)}


    {/* Fecha de nacimiento */}
    {jugador.fecha_nacimiento && (
      <p>
        <strong>Fecha de nacimiento:</strong>{" "}
        <span className="text-negro_texto">
          {new Date(jugador.fecha_nacimiento).toLocaleDateString()}
        </span>
      </p>
    )}

    {/* Estadísticas de la temporada */}
    <div className="overflow-x-auto">
      <table className="w-full text-center border-collapse">
        <thead>
          <tr className="border-b-2 border-negro_texto">
            <th className="p-1">PJ</th>
            <th className="p-1">Titular</th>
            <th className="p-1">Goles</th>
            <th className="p-1">TA</th>
            <th className="p-1">TR</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="p-1">{jugador.partidos_jugados}</td>
            <td className="p-1">{jugador.partidos_titular}</td>
            <td className="p-1">{jugador.goles}</td>
            <td className="p-1">{jugador.tarjetas_amarillas}</td>
            <td className="p-1">{jugador.tarjetas_rojas}</td>
          </tr>
        </tbody>
      </table>
    </div>

    {/* Biografía */}
    <p className="text-justify text-negro_texto font-poetsen leading-relaxed">
      {jugador.biografia}
    </p>
  </div>
</div>
</div>

    </section>
  );
}
