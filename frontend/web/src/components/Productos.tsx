import { useState, useEffect } from "react";

interface Producto {
  id_producto?: number;
  nombre: string;
  descripcion: string;
  precio: number;
  stock: number;
  imagen: string;
}

export default function Productos() {
  const [modo, setModo] = useState<
    "crear" | "listar" | "buscar" | "editar" | "eliminar"
  >("listar");
  const [nombre, setNombre] = useState("");
  const [producto, setProducto] = useState<Producto>({
    nombre: "",
    descripcion: "",
    precio: 0,
    stock: 0,
    imagen: "",
  });
  const [productos, setProductos] = useState<Producto[]>([]);

  useEffect(() => {
    if (modo === "listar") {
      fetch("http://localhost:8000/productos/")
        .then((res) => res.json())
        .then(setProductos)
        .catch((err) => console.error("Error al listar productos:", err));
    }
  }, [modo]);

  const obtenerProducto = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos/${nombre}`);
      if (res.ok) {
        const data = await res.json();
        setProducto(data);
      } else {
        alert("Producto no encontrado.");
      }
    } catch (err) {
      console.error("Error al obtener producto:", err);
    }
  };

  const crearProducto = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(producto),
      });
      if (res.ok) {
        alert("Producto creado correctamente.");
        setProducto({
          nombre: "",
          descripcion: "",
          precio: 0,
          stock: 0,
          imagen: "",
        });
        setModo("listar");
      } else {
        alert("Error al crear producto.");
      }
    } catch (err) {
      console.error("Error al crear producto:", err);
    }
  };

  const actualizarProducto = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos/${nombre}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(producto),
      });
      if (res.ok) {
        alert("Producto actualizado.");
      } else {
        alert("Error al actualizar producto.");
      }
    } catch (err) {
      console.error("Error al actualizar producto:", err);
    }
  };

  const eliminarProducto = async () => {
    try {
      const res = await fetch(`http://localhost:8000/productos/${nombre}`, {
        method: "DELETE",
      });
      if (res.ok) {
        alert("Producto eliminado.");
        setModo("listar");
      } else {
        alert("Error al eliminar producto.");
      }
    } catch (err) {
      console.error("Error al eliminar producto:", err);
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      {/* Menú de modos */}
      <div className="flex flex-wrap justify-center gap-3 mb-6 ">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
        <div className="flex justify-center">
          <button
            key={m}
            onClick={() => {
              setModo(m as any);
              setProducto({
                nombre: "",
                descripcion: "",
                precio: 0,
                stock: 0,
                imagen: "",
              });
              setNombre("");
            }}
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco ${
              modo === m ? "bg-blue-500 text-white" : "bg-white text-black"
            }`}
          >
            {m.toUpperCase()}
          </button>
          </div>
        ))}
      </div>

      {/* Input nombre para buscar/editar/eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="Nombre del producto"
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
      )}

      {/* Buscar producto */}
      {modo === "buscar" && (
  <>
    <div className="flex justify-center">
      <button
        onClick={obtenerProducto}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
      >
        Obtener Producto
      </button>
    </div>
	{producto && (
  <div className="mt-6 p-4 bg-blanco text-negro rounded-[1rem] shadow-md space-y-2">
    <p><strong>ID:</strong> {producto.id_producto}</p>
    <p><strong>Nombre:</strong> {producto.nombre}</p>
    <p><strong>Descripción:</strong> {producto.descripcion}</p>
    <p><strong>Precio:</strong> {producto.precio.toFixed(2)}€</p>
    <p><strong>Stock:</strong> {producto.stock}</p>
    {producto.imagen && (
      <img
        src={producto.imagen}
        alt={`Imagen de ${producto.nombre}`}
        className="w-24 h-24 rounded-xl mt-4 object-cover"
      />
    )}
  </div>
)}

    </>
)}


      {/* Crear producto */}
      {modo === "crear" && (
        <div className="space-y-2">
          <input
            type="text"
            placeholder="Nombre"
            value={producto.nombre}
            onChange={(e) =>
              setProducto((prev) => ({ ...prev, nombre: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="text"
            placeholder="Descripción"
            value={producto.descripcion}
            onChange={(e) =>
              setProducto((prev) => ({ ...prev, descripcion: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="number"
            placeholder="Precio"
            value={producto.precio}
            onChange={(e) =>
              setProducto((prev) => ({
                ...prev,
                precio: Number(e.target.value),
              }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="number"
            placeholder="Stock"
            value={producto.stock}
            onChange={(e) =>
              setProducto((prev) => ({
                ...prev,
                stock: Number(e.target.value),
              }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="text"
            placeholder="URL imagen"
            value={producto.imagen}
            onChange={(e) =>
              setProducto((prev) => ({ ...prev, imagen: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <div className="flex justify-center">
          <button
            onClick={crearProducto}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Crear Producto
          </button>
          </div>
        </div>
      )}

      {/* Editar producto */}
      {modo === "editar" && (
        <>
        <div className="flex justify-center">
          <button
            onClick={obtenerProducto}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Cargar Producto
          </button>
          </div>
          {producto.nombre && (
            <div className="space-y-2 mt-2">
              <input
                type="text"
                placeholder="Nombre"
                value={producto.nombre}
                onChange={(e) =>
                  setProducto((prev) => ({ ...prev, nombre: e.target.value }))
                }
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
              />
              <input
                type="text"
                placeholder="Descripción"
                value={producto.descripcion}
                onChange={(e) =>
                  setProducto((prev) => ({
                    ...prev,
                    descripcion: e.target.value,
                  }))
                }
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
              />
              <input
                type="number"
                placeholder="Precio"
                value={producto.precio}
                onChange={(e) =>
                  setProducto((prev) => ({
                    ...prev,
                    precio: Number(e.target.value),
                  }))
                }
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
              />
              <input
                type="number"
                placeholder="Stock"
                value={producto.stock}
                onChange={(e) =>
                  setProducto((prev) => ({
                    ...prev,
                    stock: Number(e.target.value),
                  }))
                }
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
              />
              <input
                type="text"
                placeholder="URL imagen"
                value={producto.imagen}
                onChange={(e) =>
                  setProducto((prev) => ({ ...prev, imagen: e.target.value }))
                }
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
              />
              <div className="flex justify-center">
              <button
                onClick={actualizarProducto}
                className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
              >
                Guardar Cambios
              </button>
              </div>
            </div>
          )}
        </>
      )}

      {/* Eliminar producto */}
      {modo === "eliminar" && (
      <div className="flex justify-center">
        <button
          onClick={eliminarProducto}
          className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Eliminar Producto
        </button>
        </div>
      )}

      {/* Listar productos */}
      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {productos.map((p) => (
            <div
              key={p.id_producto}
              className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4"
            >
              <h3 className="font-bold text-lg">{p.nombre}</h3>
              <img
                src={p.imagen}
                alt={p.nombre}
                className="w-full h-32 object-cover my-2"
              />
              <p>{p.descripcion}</p>
              <p>
                Precio: <b>{p.precio.toFixed(2)}€</b>
              </p>
              <p>Stock: {p.stock}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

