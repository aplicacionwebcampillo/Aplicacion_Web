import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-blue-700 text-white p-4 flex justify-around">
      <Link to="/" className="font-bold text-lg">Inicio</Link>
      <Link to="/plantilla">Plantilla</Link>
      <Link to="/calendario">Calendario</Link>
      <Link to="/resultados">Resultados</Link>
      <Link to="/contacto">Contacto</Link>
    </nav>
  );
}

