export default function PoliticaCookies() {
  return (
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto font-sans">
      <section className="bg-celeste text-negro_texto px-6 py-8 rounded-[1rem] font-poetsen">
        <h1 className="text-3xl font-bold mb-6 text-center">Política de Cookies</h1>

      <p className="mb-4">
        <strong>Última actualización:</strong> 4 de junio de 2025
      </p>

      <p className="mb-6">
        En <strong>CD Campillo del Río CF</strong> utilizamos cookies para mejorar tu experiencia como usuario, analizar el tráfico del sitio web y personalizar el contenido que te ofrecemos. A continuación, te explicamos en detalle qué son las cookies, qué tipos utilizamos en nuestro sitio web y cómo puedes gestionarlas.
      </p>

      <h2 className="text-2xl font-semibold mb-4">¿Qué son las cookies?</h2>
      <p className="mb-6">
        Las cookies son pequeños archivos de texto que se almacenan en tu dispositivo cuando visitas un sitio web. Estas cookies contienen información que se utiliza para mejorar tu experiencia, recordar tus preferencias, analizar cómo utilizas el sitio y ofrecer contenido personalizado según tus intereses.
      </p>

      <h2 className="text-2xl font-semibold mb-4">Tipos de cookies que utilizamos</h2>
      <p className="mb-4">
        En nuestro sitio web utilizamos diferentes tipos de cookies según su finalidad:
      </p>
      <ul className="list-disc pl-6 mb-6 space-y-2">
        <li>
          <strong>Cookies técnicas:</strong> Son imprescindibles para el correcto funcionamiento del sitio. Permiten la navegación, el acceso a áreas protegidas y el almacenamiento de tus preferencias, como el idioma o la sesión iniciada. Estas cookies no requieren consentimiento previo.
        </li>
        <li>
          <strong>Cookies de análisis (opcional):</strong> Nos permiten recopilar información sobre cómo los visitantes usan el sitio web, por ejemplo, las páginas más visitadas o los errores que se producen. Esta información nos ayuda a mejorar la experiencia del usuario y el rendimiento del sitio. Estas cookies requieren tu consentimiento previo.
        </li>
        <li>
          <strong>Cookies de terceros (opcional):</strong> Algunas funcionalidades pueden integrar servicios externos como Google Analytics, YouTube o redes sociales, que también pueden establecer cookies para ofrecer sus servicios. Estas cookies requieren tu consentimiento previo.
        </li>
      </ul>

      <h2 className="text-2xl font-semibold mb-4">¿Cómo gestionamos las cookies?</h2>
      <p className="mb-6">
        Nuestro sitio web solo utiliza actualmente <strong>cookies técnicas</strong>, por lo que no es necesario un consentimiento previo para su uso. Sin embargo, para futuras funcionalidades o servicios que requieran cookies de análisis o de terceros, implementaremos un sistema de consentimiento que te permitirá aceptarlas o rechazarlas antes de su uso.
      </p>

      <h2 className="text-2xl font-semibold mb-4">¿Cómo puedes gestionar las cookies en tu navegador?</h2>
      <p className="mb-6">
        Puedes configurar tu navegador para aceptar, rechazar o eliminar las cookies almacenadas en tu dispositivo. Ten en cuenta que si desactivas las cookies, algunas funcionalidades del sitio pueden no estar disponibles o no funcionar correctamente.
      </p>
      <p className="mb-6">
        Para ayudarte, aquí tienes enlaces a las páginas oficiales donde explican cómo gestionar las cookies en los navegadores más populares:
      </p>
      <ul className="list-disc pl-6 space-y-2 mb-8">
        <li>
          <a
            href="https://support.google.com/chrome/answer/95647?hl=es"
            target="_blank"
            rel="noopener noreferrer"
            className="text-negro_texto no-underline"
          >
            Cómo gestionar cookies en Google Chrome
          </a>
        </li>
        <li>
          <a
            href="https://support.mozilla.org/es/kb/habilitar-y-deshabilitar-cookies-sitios-web"
            target="_blank"
            rel="noopener noreferrer"
            className="text-negro_texto no-underline"
          >
            Cómo gestionar cookies en Mozilla Firefox
          </a>
        </li>
        <li>
          <a
            href="https://support.microsoft.com/es-es/microsoft-edge/eliminar-cookies-en-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09"
            target="_blank"
            rel="noopener noreferrer"
            className="text-negro_texto no-underline"
          >
            Cómo gestionar cookies en Microsoft Edge
          </a>
        </li>
      </ul>

      <h2 className="text-2xl font-semibold mb-4">Contacto</h2>
      <p>
        Si tienes cualquier duda o consulta sobre nuestra política de cookies, puedes contactarnos en:{" "}
        <a href="mailto:aplicacionwebcampillo@gmail.com." className="text-negro_texto no-underline">
          aplicacionwebcampillo@gmail.com.
        </a>
        .
      </p>
      </section>
    </main>
  );
}

