import { useEffect, useState } from "react";

export default function AvisoCookies() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const consentimiento = localStorage.getItem("cookiesAceptadas");
    if (!consentimiento) {
      setVisible(true);
    }
  }, []);

  const aceptarCookies = () => {
    localStorage.setItem("cookiesAceptadas", "true");
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <div className="fixed bottom-0 left-0 md:w-[77.5%] bg-celeste text-negro_texto p-4 flex items-center rounded-t-[1rem] md:pl-[25rem]">
      <p className="text-sm">
        Usamos cookies técnicas para mejorar tu experiencia. Puedes leer más en nuestra{" "}
        <a href="/politica-cookies" className="no-underline text-negro_texto">Política de Cookies</a>.
      </p>
      <button
        onClick={aceptarCookies}
        className="ml-[0rem] px-4 py-2 border-azul bg-blanco text-azul rounded-full hover:bg-azul  hover:text-blanco transition"
      >
        Aceptar
      </button>
    </div>
  );
}

