import { useState, useEffect } from "react";

interface Noticia {
  titular: string;
  imagen: string;
  contenido: string;
  categoria: string;
  dni_administrador: string;
}

export default function Noticias() {
  const [modo, setModo] = useState<
    "crear" | "listar" | "buscar" | "editar" | "eliminar"
  >("listar");

  const [titular, setTitular] = useState("");
  const [noticia, setNoticia] = useState<Noticia>({
    titular: "",
    imagen: "",
    contenido: "",
    categoria: "",
    dni_administrador: "",
  });

  const [noticias, setNoticias] = useState<Noticia[]>([]);

  useEffect(() => {
    if (modo === "listar") {
      fetch("http://localhost:8000/noticias/")
        .then((res) => res.json())
        .then(setNoticias)
        .catch((err) => console.error("Error al listar noticias:", err));
    }
  }, [modo]);

  const obtenerNoticia = async () => {
    try {
      const res = await fetch(`http://localhost:8000/noticias/${encodeURIComponent(titular)}`);
      if (res.ok) {
        const data = await res.json();
        setNoticia(data);
      } else {
        alert("Noticia no encontrada.");
      }
    } catch (err) {
      console.error("Error al obtener noticia:", err);
    }
  };

  const crearNoticia = async () => {
    try {
      const res = await fetch("http://localhost:8000/noticias/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(noticia),
      });
      if (res.ok) {
        alert("Noticia creada correctamente.");
        setNoticia({
          titular: "",
          imagen: "",
          contenido: "",
          categoria: "",
          dni_administrador: "",
        });
        setModo("listar");
      } else {
        alert("Error al crear noticia.");
      }
    } catch (err) {
      console.error("Error al crear noticia:", err);
    }
  };

  const actualizarNoticia = async () => {
    try {
      const res = await fetch(`http://localhost:8000/noticias/${encodeURIComponent(titular)}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(noticia),
      });
      if (res.ok) {
        alert("Noticia actualizada.");
      } else {
        alert("Error al actualizar noticia.");
      }
    } catch (err) {
      console.error("Error al actualizar noticia:", err);
    }
  };

  const eliminarNoticia = async () => {
    try {
      const res = await fetch(`http://localhost:8000/noticias/${encodeURIComponent(titular)}`, {
        method: "DELETE",
      });
      if (res.ok) {
        alert("Noticia eliminada.");
        setModo("listar");
      } else {
        alert("Error al eliminar noticia.");
      }
    } catch (err) {
      console.error("Error al eliminar noticia:", err);
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
              setNoticia({
                titular: "",
                imagen: "",
                contenido: "",
                categoria: "",
                dni_administrador: "",
              });
              setTitular("");
            }}
            className={`px-3 py-1 rounded border ${
              modo === m ? "bg-blue-500 text-white" : "bg-white text-black"
            }`}
          >
            {m.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Input titular para buscar/editar/eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="Titular de la noticia"
          className="border p-2 rounded w-full"
          value={titular}
          onChange={(e) => setTitular(e.target.value)}
        />
      )}

      {/* Buscar noticia */}
      {modo === "buscar" && (
        <>
          <button
            onClick={obtenerNoticia}
            className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
          >
            Obtener Noticia
          </button>
          {noticia.titular && (
            <div className="mt-4 border p-4 rounded shadow">
              <h3 className="text-xl font-bold mb-2">{noticia.titular}</h3>
              <img
                src={noticia.imagen}
                alt={noticia.titular}
                className="w-full h-48 object-cover mb-2"
              />
              <p><b>Categoría:</b> {noticia.categoria}</p>
              <p><b>Contenido:</b> {noticia.contenido}</p>
              <p><b>Administrador DNI:</b> {noticia.dni_administrador}</p>
            </div>
          )}
        </>
      )}

      {/* Crear noticia */}
      {modo === "crear" && (
        <div className="space-y-2">
          <input
            type="text"
            placeholder="Titular"
            value={noticia.titular}
            onChange={(e) =>
              setNoticia((prev) => ({ ...prev, titular: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            placeholder="URL Imagen"
            value={noticia.imagen}
            onChange={(e) =>
              setNoticia((prev) => ({ ...prev, imagen: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
          <textarea
            placeholder="Contenido"
            value={noticia.contenido}
            onChange={(e) =>
              setNoticia((prev) => ({ ...prev, contenido: e.target.value }))
            }
            className="border p-2 rounded w-full"
            rows={4}
          />
          <input
            type="text"
            placeholder="Categoría"
            value={noticia.categoria}
            onChange={(e) =>
              setNoticia((prev) => ({ ...prev, categoria: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            placeholder="DNI Administrador"
            value={noticia.dni_administrador}
            onChange={(e) =>
              setNoticia((prev) => ({ ...prev, dni_administrador: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
          <button
            onClick={crearNoticia}
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Crear Noticia
          </button>
        </div>
      )}

      {/* Editar noticia */}
      {modo === "editar" && (
        <>
          <button
            onClick={obtenerNoticia}
            className="bg-yellow-400 text-white px-4 py-2 rounded"
          >
            Cargar Noticia
          </button>
          {noticia.titular && (
            <div className="space-y-2 mt-2">
              <input
                type="text"
                placeholder="Titular"
                value={noticia.titular}
                onChange={(e) =>
                  setNoticia((prev) => ({ ...prev, titular: e.target.value }))
                }
                className="border p-2 rounded w-full"
              />
              <input
                type="text"
                placeholder="URL Imagen"
                value={noticia.imagen}
                onChange={(e) =>
                  setNoticia((prev) => ({ ...prev, imagen: e.target.value }))
                }
                className="border p-2 rounded w-full"
              />
              <textarea
                placeholder="Contenido"
                value={noticia.contenido}
                onChange={(e) =>
                  setNoticia((prev) => ({ ...prev, contenido: e.target.value }))
                }
                className="border p-2 rounded w-full"
                rows={4}
              />
              <input
                type="text"
                placeholder="Categoría"
                value={noticia.categoria}
                onChange={(e) =>
                  setNoticia((prev) => ({ ...prev, categoria: e.target.value }))
                }
                className="border p-2 rounded w-full"
              />
              <input
                type="text"
                placeholder="DNI Administrador"
                value={noticia.dni_administrador}
                onChange={(e) =>
                  setNoticia((prev) => ({ ...prev, dni_administrador: e.target.value }))
                }
                className="border p-2 rounded w-full"
              />
              <button
                onClick={actualizarNoticia}
                className="bg-green-500 text-white px-4 py-2 rounded"
              >
                Guardar Cambios
              </button>
            </div>
          )}
        </>
      )}

      {/* Eliminar noticia */}
      {modo === "eliminar" && (
        <button
          onClick={eliminarNoticia}
          className="bg-red-600 text-white px-4 py-2 rounded mt-2"
        >
          Eliminar Noticia
        </button>
      )}

      {/* Listar noticias */}
      {modo === "listar" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
          {noticias.map((n, i) => (
            <div
              key={i}
              className="border rounded shadow p-3 flex flex-col items-center"
            >
              <h3 className="font-bold text-lg mb-2">{n.titular}</h3>
              <img
                src={n.imagen}
                alt={n.titular}
                className="w-full h-48 object-cover mb-2"
              />
              <p><b>Categoría:</b> {n.categoria}</p>
              <p className="line-clamp-3">{n.contenido}</p>
              <p className="mt-2 text-sm text-gray-500">
                DNI Admin: {n.dni_administrador}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

