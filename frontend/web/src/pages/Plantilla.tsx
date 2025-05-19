import { useEffect, useState } from 'react';
import axios from 'axios';

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

export default function Plantilla() {
  const [jugadores, setJugadores] = useState<Jugador[]>([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/jugadores/?skip=0&limit=100')
      .then(res => setJugadores(res.data))
      .catch(err => console.error('Error al cargar jugadores:', err));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Plantilla del Equipo</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {jugadores.map((jugador) => (
          <div
            key={jugador.id_jugador}
            className="bg-white shadow-md rounded-lg p-4 flex flex-col items-center"
          >
            <div className="w-32 h-32 bg-gray-200 rounded-full mb-4 overflow-hidden">
              {jugador.foto ? (
                <img
                  src={jugador.foto}
                  alt={jugador.nombre}
                  className="object-cover w-full h-full"
                />
              ) : (
                <div className="flex items-center justify-center h-full text-gray-500">
                  Sin foto
                </div>
              )}
            </div>
            <h3 className="text-lg font-semibold">{jugador.nombre}</h3>
            <p className="text-sm text-gray-600">{jugador.posicion}</p>
            <p className="text-sm text-gray-600">Dorsal: {jugador.dorsal}</p>
            <p className="text-sm text-gray-500 text-center mt-2">{jugador.biografia}</p>
            <p className="text-xs text-gray-400 mt-1">Nacimiento: {jugador.fecha_nacimiento}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

