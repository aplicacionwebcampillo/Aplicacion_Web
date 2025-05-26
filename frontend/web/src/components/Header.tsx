import { FaFacebookF, FaInstagram, FaXTwitter, FaUser } from 'react-icons/fa6';
import { useState, useEffect } from "react";

export default function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  const userLink = isLoggedIn ? "/usuario" : "/login";
  
  const socialLinks = [
    { icon: FaInstagram, url: 'https://www.instagram.com/campillodelriocf/' },
    { icon: FaFacebookF, url: 'https://www.facebook.com/p/Campillo-del-R%C3%ADo-C-F-100078374503289/' },
    { icon: FaXTwitter, url: 'https://x.com/campillodelrio' },
  ];

  const usuarioLinks = [
    { icon: FaUser, url: userLink },
  ];

  return (
    <header className="bg-celeste text-blanco m-[0%] p-[2%]">
      <div className="flex flex-col items-center text-center space-y-6 md:space-y-0 md:flex-row md:justify-between md:items-center">

        {/* Logo */}
        <div className="md:order-1 order-1 w-full md:w-auto flex justify-center md:justify-start">
          <img
            src="/images/escudo.jpeg"
            alt="Escudo del club"
            className="h-[6rem] w-auto"
          />
        </div>

        {/* Frase central */}
        <div className="md:order-2 order-2 w-full text-center">
          <h1 className="font-bold italic font-dancing text-xl md:text-2xl lg:text-3xl [font-size:2rem]">
            UN SENTIMIENTO ALBICELESTE INALTERABLE
          </h1>
        </div>

        {/* Redes sociales */}
	<div className="md:order-3 order-3 w-full md:w-auto flex flex-row items-center justify-center md:justify-end gap-4 md:gap-6 mt-4 md:mt-0">
	  {[...socialLinks].map(({ icon: Icon, url }, index) => (
	    <a
	      key={index}
	      href={url}
	      target="_blank"
	      rel="noopener noreferrer"
	      className="w-[2rem] h-[2rem] flex items-center justify-center rounded-full bg-celeste hover:scale-110 transition-transform duration-200 shadow-lg"
	    >
	      <Icon className="text-blanco text-3xl hover:text-rojo [font-size:1.5rem]" />
	    </a>
	  ))}
	  
	  {[...usuarioLinks].map(({ icon: Icon, url }, index) => (
	    <a
	      key={index}
	      href={url}
	      rel="noopener noreferrer"
	      className="w-[2rem] h-[2rem] flex items-center justify-center rounded-full bg-celeste hover:scale-110 transition-transform duration-200 shadow-lg"
	    >
	      <Icon className="text-blanco text-3xl hover:text-rojo [font-size:1.5rem]" />
	    </a>
	  ))}
	  
	</div>

      </div>
    </header>
  );
}

