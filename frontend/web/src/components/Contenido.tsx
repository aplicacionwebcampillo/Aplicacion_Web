import { useEffect, useState } from "react";
import { useSubirImagen } from "../hooks/useSubirImagen";

type Contenido = {
  id: number;
  tipo: "texto" | "imagen";
  contenido: string;
  lugar: string;
  orden: number;
};

export default function ContenidoEstatico() {
  const { subirImagen } = useSubirImagen();

  const [modo, setModo] = useState<"crear" | "listar" | "buscar" | "editar" | "eliminar">("listar");
  const [contenidoId, setContenidoId] = useState<string>("");
  const [contenidoLugar, setContenidoLugar] = useState<string>("");
  const [contenido, setContenido] = useState<Contenido>({
    id: 0,
    tipo: "texto",
    contenido: "",
    lugar: "Equipos",
    orden: 0,
  });

  const [contenidos, setContenidos] = useState<Contenido[]>([]);
  const [lugarFiltro, setLugarFiltro] = useState<string>("");

  const lugares = ["Equipos", "Historia", "Más historia", "Palmarés", "Instalaciones"];

  useEffect(() => {
    if (modo === "listar") {
      fetchContenidos();
    }
  }, [modo]);

  const fetchContenidos = async () => {
    try {
      const res = await fetch("https://aplicacion-web-m5oa.onrender.com/contenido/");
      const data = await res.json();
      setContenidos(data);
    } catch (e) {
      console.error("Error obteniendo contenidos:", e);
    }
  };

  const obtenerContenidoPorId = async () => {
    if (!contenidoId) return alert("Debes proporcionar un ID válido");

    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/contenido/${contenidoId}`);
      if (!res.ok) throw new Error("Contenido no encontrado");
      const data = await res.json();
      setContenido(data);
    } catch (error) {
      console.error("Error al obtener contenido por ID:", error);
      alert("Error al obtener contenido");
    }
  };

  const obtenerContenidoPorLugar = async () => {
    if (!lugarFiltro) return alert("Ingresa un lugar válido");

    try {
      const res = await fetch(
        `https://aplicacion-web-m5oa.onrender.com/contenido/?lugar=${encodeURIComponent(lugarFiltro)}`
      );
      if (res.ok) {
        const data = await res.json();
        setContenidos(data);
      } else {
        alert("Contenido no encontrado para ese lugar");
      }
    } catch (e) {
      console.error("Error obteniendo contenido:", e);
      alert("Error al obtener contenido");
    }
  };

  const crearContenido = async () => {
    const res = await fetch("https://aplicacion-web-m5oa.onrender.com/contenido/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(contenido),
    });

    if (res.ok) {
      alert("Contenido creado");
      setContenido({ id: 0, tipo: "texto", contenido: "", lugar: "Equipos", orden: 0 });
      setModo("listar");
    } else {
      const error = await res.text();
      alert("Error al crear contenido: " + error);
    }
  };

  const actualizarContenido = async () => {
    if (!contenidoId) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/contenido/${contenidoId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(contenido),
      });
      if (res.ok) {
        alert("Contenido actualizado");
        setModo("listar");
      } else {
        alert("Error al actualizar contenido");
      }
    } catch (e) {
      console.error("Error actualizando contenido:", e);
    }
  };

  const eliminarContenido = async () => {
    if (!contenidoId) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/contenido/${contenidoId}`, {
        method: "DELETE",
      });
      if (res.ok) {
        alert("Contenido eliminado");
        setModo("listar");
      } else {
        alert("Error al eliminar contenido");
      }
    } catch (e) {
      console.error("Error eliminando contenido:", e);
    }
  };

  const handleImagenChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const url = await subirImagen(file);
    if (url) {
      setContenido((prev) => ({ ...prev, contenido: url }));
    } else {
      alert("Error al subir la imagen");
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[20rem] sm:max-w-[40rem] shadow-lg space-y-4">
      {/* Menú */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
          <button
            key={m}
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco ${
              modo === m ? "bg-blue-600 text-white" : "bg-white text-black"
            }`}
            onClick={() => {
              setModo(m as any);
              setContenido({ id: 0, tipo: "texto", contenido: "", lugar: "Equipos", orden: 0 });
              setContenidoId("");
              setLugarFiltro("");
              if (m === "listar") fetchContenidos();
            }}
          >
            {m.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Buscar, Editar, Eliminar - ID */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <div className="space-y-2">
          <input
            type="number"
            placeholder="ID del contenido"
            value={contenidoId}
            onChange={(e) => setContenidoId(e.target.value)}
            className="rounded-[1rem] w-[90%] border px-3 py-2"
          />
          {(modo === "buscar" || modo === "editar") && (
            <div className="flex justify-center">
            <button
              onClick={obtenerContenidoPorId}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              {modo === "buscar" ? "Buscar" : "Cargar para editar"}
            </button>
            </div>
          )}
        </div>
      )}

      {/* Mostrar resultado de búsqueda */}
      {modo === "buscar" && contenido.contenido && (
        <div className="bg-blanco text-negro p-4 rounded-[1rem] shadow space-y-2">
          <p>
            <b>Tipo:</b> {contenido.tipo.toUpperCase()}
          </p>
          <p>
            <b>Lugar:</b> {contenido.lugar}
          </p>
          <p>
            <b>Orden:</b> {contenido.orden}
          </p>
          {contenido.tipo === "texto" ? (
            <p>
              <pre className="whitespace-pre-wrap">{contenido.contenido}</pre>
            </p>
          ) : (
            <img
              src={contenido.contenido}
              alt={`Imagen contenido ${contenido.id}`}
              className="max-w-full rounded"
            />
          )}
        </div>
      )}

      {/* Crear o Editar */}
      {(modo === "crear" || (modo === "editar" && contenido.contenido)) && (
        <div className="space-y-2 max-w-md">
          <select
            value={contenido.lugar}
            onChange={(e) => setContenido((prev) => ({ ...prev, lugar: e.target.value }))}
            className="rounded-[1rem] font-poetsen w-[96%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-blanco"
          >
            {lugares.map((lugar) => (
              <option key={lugar} value={lugar}>
                {lugar}
              </option>
            ))}
          </select>

          <input
            type="number"
            placeholder="Orden del contenido"
            onChange={(e) => setContenido((prev) => ({ ...prev, orden: Number(e.target.value) }))}
            className="rounded-[1rem] font-poetsen w-[92.5%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-blanco"
          />

            <select
              value={contenido.tipo}
              onChange={(e) => setContenido((prev) => ({ ...prev, tipo: e.target.value as "texto" | "imagen" }))}
              className="rounded-[1rem] font-poetsen w-[96%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-blanco"
            >
              <option value="texto">Texto</option>
              <option value="imagen">Imagen</option>
            </select>

            <input
              type="number"
              placeholder="ID del contenido"
              onChange={(e) => setContenido((prev) => ({ ...prev, id: Number(e.target.value) }))}
              required
              className="rounded-[1rem] font-poetsen w-[92.5%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-blanco"
            />

          {/* Contenido según tipo */}
          {contenido.tipo === "texto" ? (
            <textarea
              placeholder="Contenido"
              value={contenido.contenido}
              onChange={(e) => setContenido((prev) => ({ ...prev, contenido: e.target.value }))}
              rows={5}
              className="rounded-[1rem] font-poetsen w-[92.5%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-blanco"
            />
          ) : (
            <>
              <input
                type="file"
                accept="image/*"
                onChange={handleImagenChange}
                className="w-[90%] border px-3 py-2 rounded"
              />
              {contenido.contenido && (
                <img
                  src={contenido.contenido}
                  alt=""
                  className="w-24 h-24 rounded mt-4"
                />
              )}
            </>
          )}

          <div className="flex justify-center">
            <button
              onClick={modo === "crear" ? crearContenido : actualizarContenido}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              {modo === "crear" ? "Crear Contenido" : "Guardar Cambios"}
            </button>
          </div>
        </div>
      )}

      {/* Eliminar */}
      {modo === "eliminar" && (
        <div className="flex justify-center">
          <button
            onClick={eliminarContenido}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Eliminar Contenido
          </button>
        </div>
      )}

      {/* Listar con filtro */}
      {modo === "listar" && (
        <div className="space-y-4">
          <div className="space-y-2">
            <select
              value={lugarFiltro}
              onChange={(e) => setLugarFiltro(e.target.value)}
              className="rounded-[1rem] font-poetsen w-[92.5%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-blanco"
            >
              <option value="">-- Filtrar por lugar --</option>
              {lugares.map((lugar) => (
                <option key={lugar} value={lugar}>
                  {lugar}
                </option>
              ))}
            </select>
            <div className="flex justify-center">
            <button
              onClick={obtenerContenidoPorLugar}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco "
            >
              Buscar por lugar
            </button>
            </div>
          </div>

          {contenidos.map((c) => (
            <div key={c.id} className="bg-blanco text-negro p-4 rounded-[1rem] shadow space-y-2">
              <p>
                <b>ID:</b> {c.id}
              </p>
              <p>
                <b>Tipo:</b> {c.tipo.toUpperCase()}
              </p>
              <p>
                <b>Lugar:</b> {c.lugar}
              </p>
              <p>
                <b>Orden:</b> {c.orden}
              </p>
              {c.tipo === "texto" ? (
                <pre className="whitespace-pre-wrap">{c.contenido}</pre>
              ) : (
                <img src={c.contenido} alt={`Imagen contenido ${c.id}`} className="max-w-full rounded" />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

