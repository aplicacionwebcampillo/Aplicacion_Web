const jugadores = [
  { nombre: 'Juan Pérez', posicion: 'Delantero' },
  { nombre: 'Carlos Gómez', posicion: 'Portero' },
  { nombre: 'Luis Torres', posicion: 'Defensa' }
];

export default function Plantilla() {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Plantilla</h2>
      <ul className="space-y-2">
        {jugadores.map((j, i) => (
          <li key={i} className="bg-white p-4 rounded shadow">
            <strong>{j.nombre}</strong> - {j.posicion}
          </li>
        ))}
      </ul>
    </div>
  );
}

