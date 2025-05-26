import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";

import { useCarrito } from "../context/CarritoContext";

interface Producto {
  id_producto: number;
  nombre: string;
  descripcion: string;
  precio: number;
  stock: number;
  imagen: string;
}

export default function ProductoDetalle() {
  const { nombre } = useParams();
  const [producto, setProducto] = useState<Producto | null>(null);
  const { agregarAlCarrito } = useCarrito();
  const { carrito } = useCarrito();

  useEffect(() => {
    fetch(`http://localhost:8000/productos/${nombre}`)
      .then((res) => res.json())
      .then((data) => setProducto(data))
      .catch((err) => console.error("Error al cargar producto:", err));
  }, [nombre]);

  if (!producto) {
    return <div className="text-center text-blanco mt-10">Cargando...</div>;
  }

  return (   
    <section className="text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold">
      <Link to="/tienda" className="text-negro no-underline font-semibold mb-4 inline-block hover:text-rojo">
        ← Volver a la tienda
      </Link>
      
          
      <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold flex flex-col lg:flex-row items-center gap-10">
      
        <div className="flex justify-between items-center mb-6">
        <p> </p>	
        <Link
          to="/carrito"
          className="px-6 py-2 rounded-full font-bold border-2 transition-all bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Ver carrito ({carrito.length}) 
        </Link>     
      </div>
      
        <div className="w-full max-w-[30rem]">
          <img
            src={producto.imagen || "/images/PorDefecto.png"}
            alt={producto.nombre}
            className="w-full max-w-full h-auto object-cover rounded-lg shadow-md"
          />
        </div>

        <div className="text-center lg:text-left">
          <h2 className="text-4xl mb-4">{producto.nombre}</h2>
          <p className="text-lg mb-4 text-negro">{producto.descripcion}</p>
          <p className="text-2xl text-rojo mb-2">{producto.precio} €</p>
          <p className="mb-4">
            {producto.stock > 0 ? `Stock disponible: ${producto.stock}` : "Agotado"}
          </p>

          <button
            onClick={() => agregarAlCarrito(producto, tallaSeleccionada)}
            className={`px-6 py-2 rounded-full font-bold border-2 transition-all ${
              producto.stock > 0
                ? "bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
                : "bg-gray-400 text-white cursor-not-allowed border-gray-400"
            }`}
            disabled={producto.stock === 0}
          >
            Añadir al carrito
          </button>
        </div>
      </div>
    </section>
  );
}

