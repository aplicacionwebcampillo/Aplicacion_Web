export default function PolíticaPrivacidad() {
  return (
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto font-sans">
      <section className="bg-celeste text-negro_texto px-6 py-8 rounded-[1rem] font-poetsen">
        <h1 className="text-3xl font-bold mb-6 text-center">Política de Privacidad</h1>

        <p className="mb-4">
          En <strong>CD Campillo del Río CF</strong>, nos comprometemos a garantizar la privacidad y la protección de tus datos personales en cumplimiento con el Reglamento (UE) 2016/679 (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD).
        </p>

        <h2 className="text-2xl font-semibold mt-6 mb-2">1. Responsable del tratamiento</h2>
        <p>
          El responsable del tratamiento es CD Campillo del Río CF, con domicilio social en Campillo del Río, Jaén, España. Puedes contactar con nosotros a través del correo: <strong>aplicacionwebcampillo@gmail.com</strong>.
        </p>

        <h2 className="text-2xl font-semibold mt-6 mb-2">2. Finalidad del tratamiento</h2>
        <p>
          Tratamos los datos que nos proporcionas con las siguientes finalidades:
        </p>
        <ul className="list-disc ml-6 mt-2">
          <li>Gestionar tu inscripción como jugador o socio del club.</li>
          <li>Comunicaciones relacionadas con actividades, eventos o incidencias del club.</li>
          <li>Cumplir con obligaciones legales, contables o administrativas.</li>
          <li>Garantizar la seguridad de nuestros sistemas y la trazabilidad de accesos.</li>
        </ul>

        <h2 className="text-2xl font-semibold mt-6 mb-2">3. Datos personales tratados</h2>
        <p>Los datos que recopilamos incluyen:</p>
        <ul className="list-disc ml-6 mt-2">
          <li>DNI o documento identificativo</li>
          <li>Nombre y apellidos</li>
          <li>Correo electrónico</li>
          <li>Teléfono de contacto</li>
          <li>Fecha de nacimiento</li>
        </ul>

        <h2 className="text-2xl font-semibold mt-6 mb-2">4. Base jurídica del tratamiento</h2>
        <p>
          La legitimación para el tratamiento de tus datos se basa en:
        </p>
        <ul className="list-disc ml-6 mt-2">
          <li>Tu consentimiento expreso, libre e informado.</li>
          <li>La necesidad de tratamiento para la ejecución de un contrato o precontrato (inscripción).</li>
          <li>Obligaciones legales aplicables al club como entidad deportiva.</li>
        </ul>

        <h2 className="text-2xl font-semibold mt-6 mb-2">5. Conservación de los datos</h2>
        <p>
          Tus datos se conservarán mientras exista una relación activa contigo o hasta que solicites su supresión. Posteriormente, se conservarán bloqueados durante los plazos legalmente exigidos.
        </p>

        <h2 className="text-2xl font-semibold mt-6 mb-2">6. Destinatarios de los datos</h2>
        <p>
          Tus datos no se cederán a terceros, salvo:
        </p>
        <ul className="list-disc ml-6 mt-2">
          <li>Entidades deportivas oficiales (Federaciones, Ligas, etc.).</li>
          <li>Proveedores de servicios (como hosting, software de gestión), con los que mantenemos contratos de encargo de tratamiento.</li>
          <li>Obligaciones legales impuestas a CD Campillo del Río CF.</li>
        </ul>

        <h2 className="text-2xl font-semibold mt-6 mb-2">7. Transferencias internacionales</h2>
        <p>
          No se prevén transferencias internacionales de tus datos fuera del Espacio Económico Europeo. En caso de producirse, se garantizarán las medidas adecuadas conforme a la normativa.
        </p>

        <h2 className="text-2xl font-semibold mt-6 mb-2">8. Derechos de las personas interesadas</h2>
        <p>
          Puedes ejercer tus derechos de:
        </p>
        <ul className="list-disc ml-6 mt-2">
          <li><strong>Acceso</strong> a tus datos.</li>
          <li><strong>Rectificación</strong> de datos inexactos.</li>
          <li><strong>Supresión</strong> (derecho al olvido).</li>
          <li><strong>Oposición</strong> al tratamiento.</li>
          <li><strong>Limitación</strong> del tratamiento.</li>
          <li><strong>Portabilidad</strong> de los datos.</li>
        </ul>
        <p className="mt-2">
          Para ejercer tus derechos, puedes escribirnos a <strong>aplicacionwebcampillo@gmail.com</strong> indicando el derecho que deseas ejercer y adjuntando una copia de tu documento identificativo.
        </p>

        <h2 className="text-2xl font-semibold mt-6 mb-2">9. Seguridad de los datos</h2>
        <p>
          Hemos implementado medidas técnicas y organizativas apropiadas para proteger los datos personales contra el acceso no autorizado, alteración, pérdida o destrucción.
        </p>

        <h2 className="text-2xl font-semibold mt-6 mb-2">10. Reclamaciones ante la autoridad</h2>
        <p>
          Si consideras que no hemos tratado tus datos de acuerdo con la normativa, puedes presentar una reclamación ante la Agencia Española de Protección de Datos (AEPD): <a href="https://www.aepd.es" target="_blank" className="no-underline text-negro_texto">www.aepd.es</a>.
        </p>
      </section>
    </main>
  );
}

