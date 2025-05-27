import React from "react";

export default function Palmares() {
  return (
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto font-sans">
      <section className="bg-celeste rounded-[1rem] text-negro_texto px-6 py-8 rounded-2xl font-poetsen">
        <h1 className="text-4xl text-center text-blanco font-bold mb-10">Palmarés</h1>

      <p className="mb-6">
        El Club Deportivo Campillo del Río C.F., desde su fundación, ha ido consolidándose en las competiciones regionales de fútbol, mostrando una evolución constante y un crecimiento notable en sus primeras temporadas. A continuación, se detalla su palmarés hasta la temporada 2024/2025:
      </p>

      <div className="space-y-8">
        {/* Liga */}
        <div>
          <h3 className="text-2xl text-negro_texto mb-4">Liga (Segunda Andaluza de Jaén)</h3>
          <ul className="list-disc list-inside space-y-2">
            <li>
              <strong>Temporada 2022/2023:</strong> Debut en la categoría, finalizando en la 8ª posición. Temporada de adaptación y aprendizaje.
            </li>
            <li>
              <strong>Temporada 2023/2024:</strong> Mejora de rendimiento, terminando en 5ª posición. Reflejo del crecimiento del equipo.
            </li>
            <li>
              <strong>Temporada 2024/2025:</strong> Mejor campaña hasta la fecha, acabando en 3ª posición y clasificándose para los play-offs de ascenso.
            </li>
          </ul>
        </div>

        {/* Copa */}
        <div>
          <h3 className="text-2xl text-negro_texto mb-4">Copa (Copa Subdelegada de Jaén)</h3>
          <ul className="list-disc list-inside space-y-2">
            <li>
              <strong>Temporada 2022/2023:</strong> Eliminados en octavos de final. Una experiencia formativa para el club.
            </li>
            <li>
              <strong>Temporada 2023/2024:</strong> Alcanzaron las semifinales, mostrando un progreso competitivo destacado.
            </li>
          </ul>
        </div>

        {/* Resumen */}
        <div>
          <h3 className="text-2xl text-negro_texto mb-4">Resumen del palmarés</h3>
          <ul className="list-disc list-inside space-y-2">
            <li><strong>Mejor posición en liga:</strong> 3º (Temporada 2024/2025)</li>
            <li><strong>Mejor participación en copa:</strong> Semifinales (Temporada 2023/2024)</li>
            <li><strong>Participación en play-offs de ascenso:</strong> 1 vez (Temporada 2024/2025)</li>
          </ul>
        </div>
      </div>
      </section>
    </main>
  );
}

