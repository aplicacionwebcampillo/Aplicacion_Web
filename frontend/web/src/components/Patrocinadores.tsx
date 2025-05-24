import { useEffect, useState } from "react";

interface Patrocinador {
  nombre: string;
  tipo: string;
  email: string;
  telefono: string;
  logo: string;
  fecha_inicio: string;
  fecha_fin: string;
}

export default function Patrocinadores() {
  const [patrocinadores, setPatrocinadores] = useState<Patrocinador[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/patrocinadores/")
      .then((res) => res.json())
      .then((data) => setPatrocinadores(data))
      .catch((err) => console.error("Error al cargar patrocinadores:", err));
  }, []);

  return (
    <section className="bg-white py-8 px-4 bg-celeste rounded-[1rem] text-blanco font-bold font-poetsen">
      <h2 className="text-2xl font-bold mb-6 text-center">Patrocinadores</h2>
      <div className="flex flex-wrap gap-4 pb-2 justify-center">
        {patrocinadores.map((patro, index) => (
          <div
            key={index}
            className="relative group w-40 h-40 flex-shrink-0 bg-gray-100 rounded-lg shadow-md overflow-hidden"
          >
            <img
              src={patro.logo || "/images/PorDefecto.png"}
              className="h-[15rem] w-auto object-cover"
            />
            {/* Nombre sobre el logo, solo visible en md+ */}
            <div className="absolute inset-0 bg-negro bg-opacity-70 font-bold font-poetsen flex items-center justify-center opacity-0 group-hover:opacity-30 transition-opacity hidden md:flex">
                <span className="text-center px-2">{patro.nombre}</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

