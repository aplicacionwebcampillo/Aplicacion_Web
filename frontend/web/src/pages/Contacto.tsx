import { FaMapMarkerAlt, FaPhoneAlt, FaEnvelope } from "react-icons/fa";

export default function Contacto() {
  return (
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto font-sans">
      <section className="m-0 px-4 py-12 grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
        {/* Columna izquierda: Mapa y datos de contacto */}
        <div className="bg-celeste px-4 py-8 rounded-[1rem] font-bold font-poetsen space-y-8">
  {/* Mapa */}
  <div className="w-full aspect-video">
    <iframe
      src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3145.9482372260313!2d-3.6728642476038655!3d37.95499459646416!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd6e8103176bb981%3A0xe2009a30ec2986f8!2sMunicipal%20Campillo%20Del%20Rio!5e0!3m2!1ses!2ses!4v1748384239649!5m2!1ses!2ses"
      loading="lazy"
      allowFullScreen
      referrerPolicy="no-referrer-when-downgrade"
      className="w-full h-full rounded-[1rem] border-0 shadow-md"
    ></iframe>
  </div>

  {/* Información de contacto */}
  <div className="space-y-4 text-gray-800 text-sm md:text-base">
    <div className="flex items-start gap-3">
      <FaMapMarkerAlt className="text-green-700 text-xl mt-[2px]" />
      <div>
        <p className="font-bold text-green-700 leading-[1]">Ubicación</p>
        <p className="text-negro_texto">
          Paramo Valverde, 1, 23519 Campillo del Río, Jaén
        </p>
      </div>
    </div>

    <div className="flex items-start gap-3">
      <FaPhoneAlt className="text-green-700 text-xl mt-[2px]" />
      <div>
        <p className="font-bold text-green-700 leading-[1]">Teléfono</p>
        <p className="text-negro_texto">667 885 002</p>
      </div>
    </div>

    <div className="flex items-start gap-3">
      <FaEnvelope className="text-green-700 text-xl mt-[2px]" />
      <div>
        <p className="font-bold text-green-700 leading-[1]">Correo</p>
        <p className="text-negro_texto">campillodelrio_c.f@hotmail.com</p>
      </div>
    </div>
  </div>
</div>


        {/* Columna derecha: Formulario */}
        <form
          action="https://formsubmit.co/aplicacionwebcampillo@gmail.com"
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
              className="w-[90%] rounded-[1rem] p-3 border border-gray-300 bg-gray-100"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Correo Electrónico</label>
            <input
              type="email"
              name="email"
              required
              className="w-[90%] rounded-[1rem] p-3 border border-gray-300 bg-gray-100"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Mensaje</label>
            <textarea
              name="mensaje"
              rows={6}
              required
              className="w-[90%] rounded-[1rem] p-3 border border-gray-300 bg-gray-100"
            />
          </div>

          <div className="flex justify-center mt-[1rem]">
            <button
              type="submit"
              className="px-4 py-2 rounded-full border-2 font-semibold transition-all bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
            >
              Enviar
            </button>
          </div>
        </form>
      </section>
    </main>
  );
}

