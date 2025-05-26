import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useCarrito } from "../context/CarritoContext";

function useWindowWidth() {
  const [width, setWidth] = useState<number | null>(null);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return width;
}


interface Producto {
  id_producto: number;
  nombre: string;
  precio: number;
  stock: number;
  imagen: string;
}

const FILAS_POR_PAGINA = 3;
const COLUMNAS = 3;
const PRODUCTOS_POR_PAGINA = FILAS_POR_PAGINA * COLUMNAS;

export default function TiendaMain() {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [paginaActual, setPaginaActual] = useState(1);
  const width = useWindowWidth();
  const { carrito } = useCarrito();

  useEffect(() => {
    fetch("http://localhost:8000/productos/?skip=0&limit=100")
      .then((res) => res.json())
      .then((data) => setProductos(data))
      .catch((err) => console.error("Error al cargar productos:", err));
  }, []);
  
 
  const totalPaginas = Math.ceil(productos.length / PRODUCTOS_POR_PAGINA);

  // Recortar productos de la página actual
  const productosPagina = productos.slice(
    (paginaActual - 1) * PRODUCTOS_POR_PAGINA,
    paginaActual * PRODUCTOS_POR_PAGINA
  );

  const cambiarPagina = (direccion: "anterior" | "siguiente") => {
    setPaginaActual((prev) => {
      if (direccion === "anterior" && prev > 1) return prev - 1;
      if (direccion === "siguiente" && prev < totalPaginas) return prev + 1;
      return prev;
    });
  };

  if (width === null) return null;

  return (
    <section className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold">
      <h2 className="text-3xl mb-8 text-center">Tienda Oficial</h2>
      
      <div className="flex justify-between items-center mb-6">
        <p> </p>	
        <Link
          to="/carrito"
          className="px-6 py-2 rounded-full font-bold border-2 transition-all bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Ver carrito ({carrito.length}) 
        </Link>     
      </div>
      
      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {productosPagina.map((producto) => (
          <Link to={`/tienda/${encodeURIComponent(producto.nombre)}`} key={producto.id_producto} className="no-underline">
            <div className="bg-blanco text-negro rounded-[1rem] shadow-md p-4 hover:shadow-xl transition-shadow min-h-[32rem] border-3 border-transparent hover:border-rojo">
              <div className="w-full h-64 overflow-hidden rounded-md flex justify-center items-center bg-gray-200">
                <img
                  src={producto.imagen || "/images/PorDefecto.png"}
                  alt={producto.nombre}
                  className="w-full max-w-xs h-full object-cover"
                />
              </div>
              <div className="mt-4 text-center">
                <h3 className="text-xl font-semibold">{producto.nombre}</h3>
                <p className="text-lg mt-2 text-rojo">{producto.precio} €</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
      
      {/* Paginación */}
      {width >= 640 && totalPaginas > 1 && (
        <div className="flex justify-center items-center gap-6 mt-10">
          <button
            onClick={() => cambiarPagina("anterior")}
            disabled={paginaActual === 1}
            className={`text-2xl px-3 py-1 rounded-full border ${
              paginaActual === 1
                ? "text-gray-400 border-gray-300 cursor-not-allowed"
                : "text-rojo border-rojo bg-blanco hover:bg-rojo hover:text-blanco"
            }`}
          >
            ←
          </button>
          <span className="text-lg font-bold">{paginaActual} / {totalPaginas}</span>
          <button
            onClick={() => cambiarPagina("siguiente")}
            disabled={paginaActual === totalPaginas}
            className={`text-2xl px-3 py-1 rounded-full border ${
              paginaActual === totalPaginas
                ? "text-gray-400 border-gray-300 cursor-not-allowed"
                : "text-rojo border-rojo bg-blanco hover:bg-rojo hover:text-blanco"
            }`}
          >
            →
          </button>
        </div>
      )}
      
    </section>
  );
}

