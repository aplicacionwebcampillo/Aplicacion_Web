import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
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
import Header from './components/Header';
import Footer from './components/Footer';
import "./index.css";

export default function App() {
  return (
	<Router>
	  <div className="flex flex-col min-h-screen">
	    <Header />
	    <Navbar />
	    <main className="flex-grow">
	      <Routes>
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
		<Route path="/contacto" element={<Contacto />} />
	      </Routes>
	    </main>
	    <Footer />
	  </div>
	</Router>
  );
}



