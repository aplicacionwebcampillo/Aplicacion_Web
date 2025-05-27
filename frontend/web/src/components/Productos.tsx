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
    <div className="p-4 space-y-4">
      {/* Menú de modos */}
      <div className="flex flex-wrap gap-2">
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
            className={`px-3 py-1 rounded border ${
              modo === m ? "bg-blue-500 text-white" : "bg-white text-black"
            }`}
          >
            {m.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Input nombre para buscar/editar/eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="Nombre del producto"
          className="border p-2 rounded w-full"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
      )}

      {/* Buscar producto */}
      {modo === "buscar" && (
        <>
          <button
            onClick={obtenerProducto}
            className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
          >
            Obtener Producto
          </button>
          {producto.nombre && (
            <pre className="mt-2">{JSON.stringify(producto, null, 2)}</pre>
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
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            placeholder="Descripción"
            value={producto.descripcion}
            onChange={(e) =>
              setProducto((prev) => ({ ...prev, descripcion: e.target.value }))
            }
            className="border p-2 rounded w-full"
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
            className="border p-2 rounded w-full"
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
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            placeholder="URL imagen"
            value={producto.imagen}
            onChange={(e) =>
              setProducto((prev) => ({ ...prev, imagen: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
          <button
            onClick={crearProducto}
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Crear Producto
          </button>
        </div>
      )}

      {/* Editar producto */}
      {modo === "editar" && (
        <>
          <button
            onClick={obtenerProducto}
            className="bg-yellow-400 text-white px-4 py-2 rounded"
          >
            Cargar Producto
          </button>
          {producto.nombre && (
            <div className="space-y-2 mt-2">
              <input
                type="text"
                placeholder="Nombre"
                value={producto.nombre}
                onChange={(e) =>
                  setProducto((prev) => ({ ...prev, nombre: e.target.value }))
                }
                className="border p-2 rounded w-full"
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
                className="border p-2 rounded w-full"
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
                className="border p-2 rounded w-full"
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
                className="border p-2 rounded w-full"
              />
              <input
                type="text"
                placeholder="URL imagen"
                value={producto.imagen}
                onChange={(e) =>
                  setProducto((prev) => ({ ...prev, imagen: e.target.value }))
                }
                className="border p-2 rounded w-full"
              />
              <button
                onClick={actualizarProducto}
                className="bg-green-500 text-white px-4 py-2 rounded"
              >
                Guardar Cambios
              </button>
            </div>
          )}
        </>
      )}

      {/* Eliminar producto */}
      {modo === "eliminar" && (
        <button
          onClick={eliminarProducto}
          className="bg-red-600 text-white px-4 py-2 rounded mt-2"
        >
          Eliminar Producto
        </button>
      )}

      {/* Listar productos */}
      {modo === "listar" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
          {productos.map((p) => (
            <div
              key={p.id_producto}
              className="border rounded shadow p-3 flex flex-col items-center"
            >
              <h3 className="font-bold text-lg">{p.nombre}</h3>
              <img
                src={p.imagen}
                alt={p.nombre}
                className="w-full h-32 object-cover my-2"
              />
              <p>{p.descripcion}</p>
              <p>
                Precio: <b>${p.precio.toFixed(2)}</b>
              </p>
              <p>Stock: {p.stock}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

