import React from "react";

export default function Palmares() {
  return (
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto font-sans">
      <section className="bg-celeste rounded-[1rem] text-blanco px-6 py-8 rounded-2xl font-poetsen">
        <h2 className="text-4xl font-bold text-center text-gray-800 mb-10">
          Palmarés del Club
        </h2>

        <div className="space-y-6 text-blancotext-base leading-relaxed">
          <p>
            Desde su refundación, el <strong>C.D. Campillo del Río C.F.</strong> ha demostrado una evolución constante tanto en lo deportivo como en lo institucional. A pesar de su corta trayectoria reciente, ya se han logrado importantes hitos.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8 ">
            <div className="bg-blanco text-negro p-6 rounded-xl shadow-md rounded-[1rem]">
              <h3 className="text-xl font-bold mb-2 text-rojo">🏆 Temporada 2022/2023</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>Primer partido federado tras 17 años</li>
                <li>Creación del equipo femenino</li>
                <li>Lanzamiento oficial del escudo y camisetas</li>
              </ul>
            </div>

            <div className="bg-blanco text-negro p-6 rounded-xl shadow-md rounded-[1rem]">
              <h3 className="text-xl font-bold mb-2 text-rojo">⚽ Temporada 2023/2024</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>Clasificación a la fase final del campeonato local</li>
                <li>Inauguración del campo oficial con público</li>
                <li>Consolidación de la cantera infantil</li>
              </ul>
            </div>

            <div className="bg-blanco text-negro p-6 rounded-xl shadow-md rounded-[1rem]">
              <h3 className="text-xl font-bold mb-2 text-rojo">🥇 Temporada 2024/2025</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>Subcampeón en liga provincial amateur</li>
                <li>Participación histórica en torneo regional</li>
                <li>Reconocimiento del ayuntamiento por labor deportiva</li>
              </ul>
            </div>

            <div className="bg-blanco text-negro p-6 rounded-xl shadow-md rounded-[1rem]">
              <h3 className="text-xl font-bold mb-2 text-rojo">📈 Proyecciones</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>Aspiraciones de ascenso en categorías provinciales</li>
                <li>Fomento del fútbol base en Campillo del Río</li>
                <li>Mejora de infraestructuras y equipamiento</li>
              </ul>
            </div>
          </div>

          <p className="mt-8">
            El palmarés del club es un reflejo del esfuerzo colectivo y del amor por el fútbol que existe en cada rincón de Campillo del Río. Con pasos firmes, el equipo continúa construyendo su legado.
          </p>
        </div>
      </section>
    </main>
  );
}

