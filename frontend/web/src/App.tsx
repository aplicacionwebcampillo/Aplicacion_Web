import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Logout from './pages/Logout';
import Registro from './pages/Registro';
import Usuario from './pages/Usuario';
import Socio from './pages/Socio';
import Administrador from './pages/Administrador';
import Home from './pages/Home';
import Noticias from './pages/Noticias';
import NoticiaIndividual from "./pages/NoticiaIndividual";
import Plantilla from './pages/Plantilla';
import JugadorDetalle from "./components/JugadorDetalle";
import Calendario from './pages/Calendario';
import Tienda from './pages/Tienda';
import ProductoDetalle from "./pages/ProductoDetalle";
import Carrito from "./pages/Carrito";
import Contacto from './pages/Contacto';
import Historia from './pages/Historia';
import Palmares from './pages/Palmares';
import Instalaciones from './pages/Instalaciones';
import Header from './components/Header';
import Footer from './components/Footer';
import "./index.css";
import AvisoLegal from './pages/Aviso-Legal';
import PolíticaPrivacidad from './pages/PoliticaPrivacidad';
import PoliticaCookies from './pages/PoliticaCookies';
import AvisoCookies from "./components/Cookies";
import ClubAntiguo from './pages/ClubAntiguo';

export default function App() {
  return (
	  <div className="flex flex-col min-h-screen">
	    <AvisoCookies />
	    <Header />
	    <Navbar />
	    <main className="flex-grow text-justify">
	      <Routes>
	        <Route path="/login" element={<Login />} />
	        <Route path="/logout" element={<Logout />} />
	        <Route path="/registro" element={<Registro />} />
	        <Route path="/usuario" element={<Usuario />} />
	        <Route path="/socio" element={<Socio />} />
	        <Route path="/administrador" element={<Administrador />} />
		<Route path="/" element={<Home />} />
		<Route path="/noticias" element={<Noticias />} />
		<Route path="/noticias/:titular" element={<NoticiaIndividual />} />
		<Route path="/plantilla" element={<Plantilla />} />
		<Route path="/jugadores/:id" element={<JugadorDetalle />} />
		<Route path="/calendario" element={<Calendario />} />
		<Route path="/tienda" element={<Tienda />} />
		<Route path="/tienda/:nombre" element={<ProductoDetalle />} />
		<Route path="/carrito" element={<Carrito />} />
		<Route path="/historia" element={<Historia />} />
		<Route path="/palmares" element={<Palmares />} />
		<Route path="/instalaciones" element={<Instalaciones />} />
		<Route path="/contacto" element={<Contacto />} />
		<Route path="/aviso-legal" element={<AvisoLegal />} />
		<Route path="/politica-privacidad" element={<PolíticaPrivacidad />} />
		<Route path="/politica-cookies" element={<PoliticaCookies />} />
		<Route path="/club-antiguo" element={<ClubAntiguo />} />
	      </Routes>
	    </main>
	    <Footer />
	  </div>
  );
}



