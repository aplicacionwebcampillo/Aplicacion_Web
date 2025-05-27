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
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      {/* Menú de modos */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
          <div className="flex justify-center">
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
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco ${
              modo === m ? "bg-blue-500 text-white" : "bg-white text-black"
            }`}
          >
            {m.toUpperCase()}
          </button>
          </div>
        ))}
      </div>

      {/* Input titular para buscar/editar/eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="Titular de la noticia"
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          value={titular}
          onChange={(e) => setTitular(e.target.value)}
        />
      )}

      {/* Buscar noticia */}
      {modo === "buscar" && (
        <>
        <div className="flex justify-center">
          <button
            onClick={obtenerNoticia}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Obtener Noticia
          </button>
          </div>
          {noticia.titular && (
            <div className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4">
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
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="text"
            placeholder="URL Imagen"
            value={noticia.imagen}
            onChange={(e) =>
              setNoticia((prev) => ({ ...prev, imagen: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <textarea
            placeholder="Contenido"
            value={noticia.contenido}
            onChange={(e) =>
              setNoticia((prev) => ({ ...prev, contenido: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
            rows={4}
          />
          <input
            type="text"
            placeholder="Categoría"
            value={noticia.categoria}
            onChange={(e) =>
              setNoticia((prev) => ({ ...prev, categoria: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="text"
            placeholder="DNI Administrador"
            value={noticia.dni_administrador}
            onChange={(e) =>
              setNoticia((prev) => ({ ...prev, dni_administrador: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <div className="flex justify-center">
          <button
            onClick={crearNoticia}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Crear Noticia
          </button>
          </div>
        </div>
      )}

      {/* Editar noticia */}
      {modo === "editar" && (
        <>
        <div className="flex justify-center">
          <button
            onClick={obtenerNoticia}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Cargar Noticia
          </button>
          </div>
          {noticia.titular && (
            <div className="space-y-2 mt-2">
              <input
                type="text"
                placeholder="Titular"
                value={noticia.titular}
                onChange={(e) =>
                  setNoticia((prev) => ({ ...prev, titular: e.target.value }))
                }
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
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
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
                rows={4}
              />
              <input
                type="text"
                placeholder="Categoría"
                value={noticia.categoria}
                onChange={(e) =>
                  setNoticia((prev) => ({ ...prev, categoria: e.target.value }))
                }
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
              />
              <input
                type="text"
                placeholder="DNI Administrador"
                value={noticia.dni_administrador}
                onChange={(e) =>
                  setNoticia((prev) => ({ ...prev, dni_administrador: e.target.value }))
                }
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
              />
              <div className="flex justify-center">
              <button
                onClick={actualizarNoticia}
                className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
              >
                Guardar Cambios
              </button>
              </div>
            </div>
          )}
        </>
      )}

      {/* Eliminar noticia */}
      {modo === "eliminar" && (
      <div className="flex justify-center">
        <button
          onClick={eliminarNoticia}
          className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Eliminar Noticia
        </button>
        </div>
      )}

      {/* Listar noticias */}
      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {noticias.map((n, i) => (
            <div
              key={i}
              className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4"
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

