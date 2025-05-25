import UltimasNoticias from "../components/UltimasNoticias";
import Clasificacion from "../components/Clasificacion";
import Patrocinadores from "../components/Patrocinadores";
import Partidos from "../components/Partidos";



export default function Home() {
  return (
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto m-[0%] p-[2%] font-sans">
    	<UltimasNoticias />
    	<Partidos />
    	<Clasificacion />
    	<Patrocinadores />
    </main>
  );
}

