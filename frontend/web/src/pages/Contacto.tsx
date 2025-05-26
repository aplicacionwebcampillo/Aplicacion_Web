export default function Contacto() {
  return (
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto font-sans ">
    <section className="m-[0rem] px-4 py-12 grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
  {/* Columna izquierda: Mapa y datos de contacto */}
  <div className="bg-celeste px-4 py-8 rounded-[1rem] font-bold font-poetsen ">

    {/* Información de contacto */}
    <div className="space-y-4 text-gray-800 text-sm md:text-base">
      <div className="flex items-center gap-3">
        <span className="text-green-700 text-xl">📍</span>
        <div>
          <p className="font-bold text-green-700">Ubicación</p>
          <p>Paramo Valverde, 1, 23519 Campillo del Río, Jaén</p>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-green-700 text-xl">📞</span>
        <div>
          <p className="font-bold text-green-700">Teléfono</p>
          <p>667 885 002</p>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-green-700 text-xl">📧</span>
        <div>
          <p className="font-bold text-green-700">Correo</p>
          <p>campillodelrio_c.f@hotmail.com</p>
        </div>
      </div>
    </div>
  </div>

  {/* Columna derecha: Formulario */}
  <form
    action="https://formsubmit.co/campillodelrio_c.f@hotmail.com"
    method="POST"
    className="bg-celeste text-black px-4 py-8 rounded-[1rem] font-bold font-poetsen"
  >
    <input type="hidden" name="_captcha" value="false" />
    <input type="hidden" name="_next" value="/contacto" />

    <div>
      <label className="block text-sm font-medium mb-1">Nombre</label>
      <input
        type="text"
        name="nombre"
        required
        className="w-[90%] rounded-[1rem] p-3 border border-gray-300 rounded-md bg-gray-100"
      />
    </div>

    <div>
      <label className="block text-sm font-medium mb-1">Correo Electrónico</label>
      <input
        type="email"
        name="email"
        required
        className="w-[90%] rounded-[1rem] p-3 border border-gray-300 rounded-md bg-gray-100"
      />
    </div>


    <div>
      <label className="block text-sm font-medium mb-1">Mensaje</label>
      <textarea
        name="mensaje"
        rows={6}
        required
        className="w-[90%] rounded-[1rem] p-3 border border-gray-300 rounded-md bg-gray-100"
      />
    </div>

    <div className="flex justify-center mt-[1rem]">
    <button
      type="submit"
      className="px-4 py-2 rounded-full border-2 font-semibold transition-all px-4 py-2 rounded-full border-2 font-semibold transition-all bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
    >
      Enviar
    </button>
    </div>
    
  </form>
</section>

   </main>
  );
}

