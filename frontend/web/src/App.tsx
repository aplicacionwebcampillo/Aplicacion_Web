import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Noticias from './pages/Noticias';
import NoticiaIndividual from "./pages/NoticiaIndividual";
import Plantilla from './pages/Plantilla';
import JugadorDetalle from "./components/JugadorDetalle";
import Calendario from './pages/Calendario';
import Resultados from './pages/Resultados';
import Contacto from './pages/Contacto';
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
		<Route path="/resultados" element={<Resultados />} />
		<Route path="/contacto" element={<Contacto />} />
	      </Routes>
	    </main>
	    <Footer />
	  </div>
	</Router>
  );
}



