import { useEffect, useState } from "react";

interface Clasificacion {
  nombre_competicion: string;
  temporada_competicion: string;
  equipo: string;
  posicion: number;
  puntos: number;
}

export default function Clasificacion() {
  const [datos, setDatos] = useState<Clasificacion[]>([]);

  useEffect(() => {
    fetch(
      "http://localhost:8000/clasificaciones?nombre_competicion=2ª%20Andaluza%20Sénior%20(Jaén)&temporada_competicion=Temporada%202024-2025"
    )
      .then((res) => res.json())
      .then((data) => setDatos(data))
      .catch((err) => console.error("Error al cargar la clasificación:", err));
  }, []);

  return (
    <section className="bg-celeste text-black px-4 py-8 text-blanco rounded-[1rem] font-bold font-poetsen">
      <h2 className="text-2xl font-bold mb-6 text-center">Clasificación</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full table-auto border-[0.2rem] border-rojo bg-blanco text-negro rounded-[1rem]">
          <thead className="bg-gray-200 text-center rounded-[1rem]">
            <tr>
              <th className="px-4 py-2">Posición</th>
              <th className="px-4 py-2">Equipo</th>
              <th className="px-4 py-2">Puntos</th>
            </tr>
          </thead>
          <tbody>
            {datos
              .sort((a, b) => a.posicion - b.posicion)
              .map((fila, index) => (
                <tr key={index} className="hover:bg-gray-100">
                  <td className="px-4 py-2 border-t">{fila.posicion}</td>
                  <td className="px-4 py-2 border-t">{fila.equipo}</td>
                  <td className="px-4 py-2 border-t">{fila.puntos}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

