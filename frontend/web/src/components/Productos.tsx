// components/Productos.tsx

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
      fetch("https://aplicacion-web-m5oa.onrender.com/productos/")
        .then((res) => res.json())
        .then(setProductos)
        .catch((err) => console.error("Error al listar productos:", err));
    }
  }, [modo]);

  const handleImagenChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", "Aplicacion_Web");

    try {
      const res = await fetch(
        "https://api.cloudinary.com/v1_1/dft3xbtrl/image/upload",
        {
          method: "POST",
          body: formData,
        }
      );
      const data = await res.json();
      setProducto((prev) => ({ ...prev, imagen: data.secure_url }));
    } catch (err) {
      console.error("Error al subir la imagen:", err);
      alert("Error al subir imagen.");
    }
  };

  const obtenerProducto = async () => {
    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/productos/${nombre}`);
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
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/productos/`, {
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
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/productos/${nombre}`, {
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
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/productos/${nombre}`, {
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
      {/* Menú */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
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
              modo === m
                ? "bg-blue-500 text-azul"
                : "bg-blanco text-black border-azul hover:bg-azul hover:text-blanco"
            }`}
          >
            {m.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Nombre para buscar/editar/eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="Nombre del producto"
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
      )}

      {/* Buscar */}
      {modo === "buscar" && (
        <>
          <div className="flex justify-center">
            <button
              onClick={obtenerProducto}
              className="px-4 py-2 rounded-full border-2 font-bold bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
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

      {/* Crear */}
      {modo === "crear" && (
        <div className="space-y-2">
          <input type="text" placeholder="Nombre" value={producto.nombre} onChange={(e) => setProducto((p) => ({ ...p, nombre: e.target.value }))} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
          <input type="text" placeholder="Descripción" value={producto.descripcion} onChange={(e) => setProducto((p) => ({ ...p, descripcion: e.target.value }))} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
          <input type="number" placeholder="Precio" value={producto.precio} onChange={(e) => setProducto((p) => ({ ...p, precio: +e.target.value }))} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
          <input type="number" placeholder="Stock" value={producto.stock} onChange={(e) => setProducto((p) => ({ ...p, stock: +e.target.value }))} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
          <input type="file" accept="image/*" onChange={handleImagenChange} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
          {producto.imagen && <img src={producto.imagen} alt="Vista previa" className="w-24 h-24 object-cover rounded-xl" />}
          <div className="flex justify-center">
            <button onClick={crearProducto} className="px-4 py-2 rounded-full border-2 font-bold bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">Crear Producto</button>
          </div>
        </div>
      )}

      {/* Editar */}
      {modo === "editar" && (
        <>
          <div className="flex justify-center">
            <button
              onClick={obtenerProducto}
              className="px-4 py-2 rounded-full border-2 font-bold bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              Cargar Producto
            </button>
          </div>
          {producto.nombre && (
            <div className="space-y-2 mt-2">
              <input type="text" placeholder="Nombre" value={producto.nombre} onChange={(e) => setProducto((p) => ({ ...p, nombre: e.target.value }))} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
              <input type="text" placeholder="Descripción" value={producto.descripcion} onChange={(e) => setProducto((p) => ({ ...p, descripcion: e.target.value }))} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
              <input type="number" placeholder="Precio" value={producto.precio} onChange={(e) => setProducto((p) => ({ ...p, precio: +e.target.value }))} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
              <input type="number" placeholder="Stock" value={producto.stock} onChange={(e) => setProducto((p) => ({ ...p, stock: +e.target.value }))} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
              <input type="file" accept="image/*" onChange={handleImagenChange} className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
              {producto.imagen && <img src={producto.imagen} alt="Vista previa" className="w-24 h-24 object-cover rounded-xl" />}
              <div className="flex justify-center">
                <button onClick={actualizarProducto} className="px-4 py-2 rounded-full border-2 font-bold bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">Guardar Cambios</button>
              </div>
            </div>
          )}
        </>
      )}

      {/* Eliminar */}
      {modo === "eliminar" && (
        <div className="flex justify-center">
          <button
            onClick={eliminarProducto}
            className="px-4 py-2 rounded-full border-2 font-bold bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Eliminar Producto
          </button>
        </div>
      )}

      {/* Listar */}
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
              <p>Precio: <b>{p.precio.toFixed(2)}€</b></p>
              <p>Stock: {p.stock}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

