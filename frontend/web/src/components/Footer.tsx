import { FaFacebookF, FaInstagram, FaXTwitter} from 'react-icons/fa6';
import { FaMapMarkerAlt } from 'react-icons/fa';

export default function Footer() {
  const socialLinks = [
    { icon: FaInstagram, url: 'https://www.instagram.com/campillodelriocf/' },
    { icon: FaFacebookF, url: 'https://www.facebook.com/p/Campillo-del-R%C3%ADo-C-F-100078374503289/' },
    { icon: FaXTwitter, url: 'https://x.com/campillodelrio' },
    { icon: FaMapMarkerAlt, url: 'https://maps.app.goo.gl/BgnLWnAuvcGHYXq77' }
  ];

  return (
    <footer className="bg-celeste text-blanco text-center py-6 mt-10 text-sm md:text-base rounded-t-[1rem]">
      <div className="flex flex-wrap justify-center items-center gap-x-8 gap-y-4">
      
        <p>
          <a href="/aviso-legal" className="no-underline text-blanco  hover:text-azul transition-colors ">
            Aviso Legal
          </a>
        </p>
        
        <p>
          <a href="/politica-privacidad" className="no-underline text-blanco  hover:text-azul transition-colors ">
            Política de Privacidad
          </a>
        </p>
        
        <p>
          <a href="/politica-cookies" className="no-underline text-blanco  hover:text-azul transition-colors ">
            Política de Cookies
          </a>
        </p>
        
        <p>
          <a href="contacto" className="no-underline text-blanco  hover:text-azul transition-colors ">
            Contacto
          </a>
        </p>
        
        <p className="md:order-3 order-3 w-full md:w-auto flex flex-row items-center justify-center md:justify-end gap-4 md:gap-6">
	  {[...socialLinks].map(({ icon: Icon, url }, index) => (
	    <a
	      key={index}
	      href={url}
	      target="_blank"
	      rel="noopener noreferrer"
	      className="w-[1rem] h-[1rem] flex items-center justify-center rounded-full bg-celeste hover:scale-110 transition-transform duration-200 shadow-lg"
	    >
	      <Icon className="text-blanco text-3xl hover:text-azul [font-size:1rem]" />
	    </a>
	  ))}
        </p>
        </div>
        
        <div className="max-w-5xl mx-auto px-4 space-y-2">
        <p>
          © {new Date().getFullYear()} <a href="/" className="no-underline text-blanco  hover:text-azul transition-colors ">
            <strong> Campillo del Río C.F. </strong>
          </a> Todos los derechos reservados.
        </p>
        <p>
          Desarrollado por <a href="https://www.linkedin.com/in/gabriel-vico-arboledas-277189330/" target="_blank" className="no-underline text-blanco  hover:text-azul transition-colors ">
            <strong> Gabriel Vico Arboledas </strong>
          </a> en colaboración con la
          <a href="https://www.ugr.es/" target="_blank"className="no-underline text-blanco  hover:text-azul transition-colors ">
            <strong> Universidad de Granada (UGR) </strong>
          </a>.
        </p>
      </div>
    </footer>
  );
}

