import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";

import { useCarrito } from "../context/CarritoContext";
import { useAuth } from "../context/useAuth"; // ajusta la ruta si hace falta

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
  const { agregarAlCarrito, carrito } = useCarrito();
  const { usuario } = useAuth();
  const navigate = useNavigate();

  const [tallaSeleccionada, setTallaSeleccionada] = useState("M"); 

  useEffect(() => {
    fetch(`https://aplicacion-web-m5oa.onrender.com/productos/${nombre}`)
      .then((res) => res.json())
      .then((data) => setProducto(data))
      .catch((err) => console.error("Error al cargar producto:", err));
  }, [nombre]);

  if (!producto) {
    return <div className="text-center text-blanco mt-10">Cargando...</div>;
  }

  const handleAgregar = () => {
    if (!usuario) {
      alert("Debes iniciar sesión para poder comprar.");
      navigate("/login");
      return;
    }
    agregarAlCarrito(producto, tallaSeleccionada);
  };

  return (
    <section className="text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold">
      <Link
        to="/tienda"
        className="text-negro no-underline font-semibold mb-4 inline-block hover:text-azul"
      >
        ← Volver a la tienda
      </Link>

      <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold flex flex-col items-center justify-center gap-10 max-w-[60rem] mx-auto">

        <div className="flex justify-between items-center mb-6 w-full">
          <p> </p>
          <Link
            to="/carrito"
            className="px-6 py-2 rounded-full font-bold border-2 transition-all bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
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

        <div className="text-center w-full max-w-[30rem]">
          <h2 className="text-4xl mb-4">{producto.nombre}</h2>
          <p className="text-lg mb-4 text-negro">{producto.descripcion}</p>
          <p className="text-2xl text-azul mb-2">{producto.precio} €</p>
          <p className="mb-4">
            {producto.stock > 0 ? `Stock disponible` : "Agotado"}
          </p>

          {/* Selector de talla */}
          <div className="mb-4">
            <label htmlFor="talla" className="mr-2 font-semibold text-negro">
              Selecciona talla:
            </label>
            <select
              id="talla"
              value={tallaSeleccionada}
              onChange={(e) => setTallaSeleccionada(e.target.value)}
              className="rounded-[1rem] font-poetsen rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            >
              <option value="4">4</option>
              <option value="6">6</option>
              <option value="8">8</option>
              <option value="10">10</option>
              <option value="12">12</option>
              <option value="14">14</option>
              <option value="S">S</option>
              <option value="M">M</option>
              <option value="L">L</option>
              <option value="XL">XL</option>
              <option value="XXL">XXL</option>
              <option value="3XL">3XL</option>
            </select>
          </div>

          <button
            onClick={handleAgregar}
            className={`px-6 py-2 rounded-full font-bold border-2 transition-all ${
              producto.stock > 0
                ? "bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
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

