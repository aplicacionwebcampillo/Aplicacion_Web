import { useState } from 'react';
import { NavLink } from 'react-router-dom';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const menuItems = [
    { to: '/', label: 'Inicio' },
    { to: '/plantilla', label: 'Plantilla' },
    { to: '/calendario', label: 'Calendario' },
    { to: '/resultados', label: 'Resultados' },
    { to: '/contacto', label: 'Contacto' },
  ];

  return (
    <nav className="bg-celeste text-blanco p-0">
      {/* Botón hamburguesa centrado en móvil */}
      <div className="flex justify-center md:hidden">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="text-blanco text-[1.5rem] font-bold border-none shadow-none focus:outline-none focus:shadow-none bg-celeste border-cerleste"
          aria-label="Toggle menu"
        >
          <span className="text-[2rem]">{isOpen ? '⨯' : '☰ '}</span>
        </button>
      </div>

      {/* Menú responsive */}
      <div
        className={`
          ${isOpen ? 'block' : 'hidden'}
          mt-0 md:mt-0
          md:flex md:justify-between md:items-center md:w-full p-0
        `}
      >
        <ul className="list-none flex flex-col md:flex-row md:justify-between w-full justify-center items-center list-none p-0 m-0 md:pl-24 pr-24">
          {menuItems.map(({ to, label }) => (
            <li key={to} className="w-full md:w-auto text-center font-bold font-poetsen">
              <NavLink
                to={to}
                onClick={() => setIsOpen(false)}
                className={({ isActive }) =>
                  `block py-2 font-bold text-lg no-underline ${
                    isActive ? 'text-rojo' : 'text-blanco'
                  } hover:text-rojo`
                }
              >
                {label}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}

