import { useState } from 'react';
import { NavLink } from 'react-router-dom';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [openSubmenu, setOpenSubmenu] = useState<string | null>(null);

  const menuItems = [
    { to: '/', label: 'Inicio' },
    { to: '/noticias', label: 'Noticias' },
    {
      label: 'Equipos',
      submenu: [
        { to: '/plantilla', label: 'Plantillas' },
        { to: '/calendario', label: 'Calendarios' },
      ],
    },
    { to: '/tienda', label: 'Tienda' },
    {
      label: 'Club',
      submenu: [
        { to: '/historia', label: 'Historia' },
        { to: '/palmares', label: 'Palmarés' },
        { to: '/instalaciones', label: 'Instalaciones' },
        { to: '/contacto', label: 'Contacto' },
      ],
    },
  ];

  const toggleSubmenu = (label: string) => {
    setOpenSubmenu(openSubmenu === label ? null : label);
  };

  return (
    <nav className="bg-celeste text-blanco p-0 rounded-b-[1rem]">
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
        <ul className="list-none flex flex-col md:flex-row md:justify-between w-full justify-center items-center list-none p-0 m-0 md:pl-[10rem] pr-[10rem] ">
          {menuItems.map((item) => (
            <li
              key={item.label}
              className="w-full md:w-auto text-center font-bold font-poetsen relative group"
              onMouseEnter={() => item.submenu && setOpenSubmenu(item.label)}
              onMouseLeave={() => item.submenu && setOpenSubmenu(null)}
            >
              {item.submenu ? (
                <>
                  <button
                    onClick={() => toggleSubmenu(item.label)}
                    className="py-2 text-[1.4rem] font-poetsen font-bold text-lg no-underline text-blanco hover:text-azul border-none shadow-none focus:outline-none focus:shadow-none bg-celeste border-celeste"
                  >
                    {item.label}
                  </button>
                  <ul
                    className={`
                      ${openSubmenu === item.label ? 'block' : 'hidden'}
                      md:absolute md:left-0 md:top-full bg-celeste md:border-2 border-azul md:rounded-b-lg shadow-md
                      md:min-w-[10rem] text-left z-50 rounded-[1rem] p-[0]
                    `}
                  >
                    {item.submenu.map((sub) => (
                      <li key={sub.to}>
                        <NavLink
                          to={sub.to}
                          onClick={() => {
                            setIsOpen(false);
                            setOpenSubmenu(null);
                          }}
                          className={({ isActive }) =>
                            `block px-4 py-2 text-sm font-poetsen text-[1.4rem] ${
                              isActive ? 'text-azul' : 'text-blanco'
                            } hover:text-azul hover:bg-celeste md:hover:bg-celeste rounded-[1rem] text-center no-underline`
                          }
                        >
                          {sub.label}
                        </NavLink>
                      </li>
                    ))}
                  </ul>
                </>
              ) : (
                <NavLink
                  to={item.to!}
                  onClick={() => setIsOpen(false)}
                  className={({ isActive }) =>
                    `block py-2 font-bold text-lg text-[1.4rem] no-underline ${
                      isActive ? 'text-azul' : 'text-blanco'
                    } hover:text-azul`
                  }
                >
                  {item.label}
                </NavLink>
              )}
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}

