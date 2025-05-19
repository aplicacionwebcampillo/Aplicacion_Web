import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Plantilla from './pages/Plantilla';
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
		<Route path="/plantilla" element={<Plantilla />} />
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



