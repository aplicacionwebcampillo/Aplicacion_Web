import { useState, useEffect } from "react";
import { useSubirImagen } from "../hooks/useSubirImagen";

interface Noticia {
  id_noticia: string,
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

  // Hook para subir imagen
  const { subirImagen, loading: cargandoImagen, error: errorImagen } = useSubirImagen();
  const [titular, setTitular] = useState("");
  const [noticia, setNoticia] = useState<Noticia>({
    id_noticia: "",
    titular: "",
    imagen: "",
    contenido: "",
    categoria: "",
    dni_administrador: "",
  });

  const [noticias, setNoticias] = useState<Noticia[]>([]);

  useEffect(() => {
    if (modo === "listar") {
      fetch("https://aplicacion-web-m5oa.onrender.com/noticias/")
        .then((res) => res.json())
        .then(setNoticias)
        .catch((err) => console.error("Error al listar noticias:", err));
    }
  }, [modo]);

  const obtenerNoticia = async () => {
    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/noticias/${encodeURIComponent(titular)}`);
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
      const res = await fetch("https://aplicacion-web-m5oa.onrender.com/noticias/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(noticia),
      });
      if (res.ok) {
        alert("Noticia creada correctamente.");
        setNoticia({
          id_noticia: "",
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
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/noticias/${encodeURIComponent(titular)}`, {
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
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/noticias/${encodeURIComponent(titular)}`, {
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

  const handleImagenChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const url = await subirImagen(file);
      if (url) {
        setNoticia((prev) => ({ ...prev, imagen: url }));
      } else {
        alert("Error al subir la imagen");
      }
    } catch (error) {
      alert("Error al subir la imagen");
      console.error(error);
    }
  };

  const ImagenInput = (
    <>
      <input
        type="file"
        accept="image/*"
        onChange={handleImagenChange}
        className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
      />
      {cargandoImagen && <p className="text-yellow-400 text-sm">Subiendo imagen...</p>}
      {errorImagen && <p className="text-red-600 text-sm">{errorImagen}</p>}
      {noticia.imagen && (
        <img
          src={noticia.imagen}
          alt="Vista previa"
          className="mt-2 w-full h-48 object-cover rounded-xl"
        />
      )}
    </>
  );

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      {/* Menú de modos */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
          <div className="flex justify-center" key={m}>
            <button
              onClick={() => {
                setModo(m as any);
                setNoticia({
                  id_noticia: "",
                  titular: "",
                  imagen: "",
                  contenido: "",
                  categoria: "",
                  dni_administrador: "",
                });
                setTitular("");
              }}
              className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 ${
                modo === m ? "bg-azul text-blanco border-azul" : "bg-blanco text-azul border-azul"
              }`}
            >
              {m.toUpperCase()}
            </button>
          </div>
        ))}
      </div>

      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="Titular de la noticia"
          className="rounded-[1rem] font-poetsen w-[90%] border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          value={titular}
          onChange={(e) => setTitular(e.target.value)}
        />
      )}

      {modo === "buscar" && (
        <>
          <div className="flex justify-center">
            <button
              onClick={obtenerNoticia}
              className="px-4 py-2 rounded-full border-2 font-bold bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              Obtener Noticia
            </button>
          </div>
          {noticia.titular && (
            <div className="bg-blanco text-negro px-6 py-10 rounded-[1rem] shadow-lg space-y-4">
              <h3 className="text-xl font-bold">{noticia.titular}</h3>
              <img src={noticia.imagen} alt={noticia.titular} className="w-full h-48 object-cover" />
              <p><b>Categoría:</b> {noticia.categoria}</p>
              <p><b>Contenido:</b> {noticia.contenido}</p>
              <p><b>Administrador DNI:</b> {noticia.dni_administrador}</p>
            </div>
          )}
        </>
      )}

      {(modo === "crear" || (modo === "editar" && noticia.titular)) && (
        <div className="space-y-2">
          <input
            type="text"
            placeholder="Titular"
            value={noticia.titular}
            onChange={(e) => setNoticia({ ...noticia, titular: e.target.value })}
            className="rounded-[1rem] font-poetsen w-[90%] border border-gray-300 px-3 py-2"
          />
          {ImagenInput}
          <textarea
            placeholder="Contenido"
            value={noticia.contenido}
            onChange={(e) => setNoticia({ ...noticia, contenido: e.target.value })}
            className="rounded-[1rem] font-poetsen w-[90%] border border-gray-300 px-3 py-2"
            rows={4}
          />
          <input
            type="text"
            placeholder="Categoría"
            value={noticia.categoria}
            onChange={(e) => setNoticia({ ...noticia, categoria: e.target.value })}
            className="rounded-[1rem] font-poetsen w-[90%] border border-gray-300 px-3 py-2"
          />
          <input
            type="text"
            placeholder="DNI Administrador"
            value={noticia.dni_administrador}
            onChange={(e) => setNoticia({ ...noticia, dni_administrador: e.target.value })}
            className="rounded-[1rem] font-poetsen w-[90%] border border-gray-300 px-3 py-2"
          />
          <div className="flex justify-center">
            <button
              onClick={modo === "crear" ? crearNoticia : actualizarNoticia}
              className="px-4 py-2 rounded-full border-2 font-bold bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              {modo === "crear" ? "Crear Noticia" : "Guardar Cambios"}
            </button>
          </div>
        </div>
      )}

      {modo === "editar" && !noticia.titular && (
        <div className="flex justify-center">
          <button
            onClick={obtenerNoticia}
            className="px-4 py-2 rounded-full border-2 font-bold bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Cargar Noticia
          </button>
        </div>
      )}

      {modo === "eliminar" && (
        <div className="flex justify-center">
          <button
            onClick={eliminarNoticia}
            className="px-4 py-2 rounded-full border-2 font-bold bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Eliminar Noticia
          </button>
        </div>
      )}

      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {noticias.map((n, i) => (
            <div key={i} className="bg-blanco text-negro px-6 py-10 rounded-[1rem] shadow-lg space-y-4">
              <h3 className="text-lg font-bold">{n.titular}</h3>
              <img src={n.imagen} alt={n.titular} className="w-full h-48 object-cover" />
              <p><b>Categoría:</b> {n.categoria}</p>
              <p className="line-clamp-3">{n.contenido}</p>
              <p className="text-sm text-gray-500">DNI Admin: {n.dni_administrador}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

