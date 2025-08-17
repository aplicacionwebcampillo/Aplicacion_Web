import { useState, useEffect } from "react";
import { useSubirImagen } from "../hooks/useSubirImagen";

interface Jugador {
  nombre: string;
  posicion: string;
  fecha_nacimiento: string;
  foto: string;
  biografia: string;
  dorsal: number | null;
  id_equipo: number;
  id_jugador?: number;
}

export default function Jugadores() {
  const [modo, setModo] = useState<
    "crear" | "listar" | "buscar" | "editar" | "eliminar"
  >("listar");

  const [jugadorNombreBuscado, setJugadorNombreBuscado] = useState<string>("");
  const [isDate, setIsDate] = useState(false);

  const [jugador, setJugador] = useState<Jugador>({
    nombre: "",
    posicion: "",
    fecha_nacimiento: "",
    foto: "",
    biografia: "",
    dorsal: null,
    id_equipo: 0,
  });

  const [jugadores, setJugadores] = useState<Jugador[]>([]);

  const { subirImagen, loading: imagenCargando, error: errorImagen } = useSubirImagen();

  useEffect(() => {
    if (modo === "listar") {
      fetch("https://aplicacion-web-m5oa.onrender.com/jugadores/")
        .then((res) => res.json())
        .then(setJugadores)
        .catch((e) => console.error("Error listando jugadores:", e));
    }
  }, [modo]);

  const obtenerJugador = async () => {
    if (!jugadorNombreBuscado) return alert("Ingresa un nombre válido");
    try {
      const res = await fetch(
        `https://aplicacion-web-m5oa.onrender.com/jugadores/${encodeURIComponent(jugadorNombreBuscado)}`
      );
      if (res.ok) {
        const data = await res.json();
        setJugador(data);
      } else {
        alert("Jugador no encontrado");
      }
    } catch (error) {
      console.error("Error obteniendo jugador:", error);
    }
  };

  const crearJugador = async () => {
    try {
      const res = await fetch("https://aplicacion-web-m5oa.onrender.com/jugadores/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jugador),
      });
      if (res.ok) {
        alert("Jugador creado");
        setJugador({
          nombre: "",
          posicion: "",
          fecha_nacimiento: "",
          foto: "",
          biografia: "",
          dorsal: null,
          id_equipo: 0,
        });
        setModo("listar");
      } else {
        alert("Error al crear jugador");
      }
    } catch (error) {
      console.error("Error creando jugador:", error);
    }
  };

  const actualizarJugador = async () => {
    if (!jugadorNombreBuscado) return alert("Ingresa un nombre válido");
    try {
      const res = await fetch(
        `https://aplicacion-web-m5oa.onrender.com/jugadores/${encodeURIComponent(jugadorNombreBuscado)}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(jugador),
        }
      );
      if (res.ok) {
        alert("Jugador actualizado");
      } else {
        alert("Error al actualizar jugador");
      }
    } catch (error) {
      console.error("Error actualizando jugador:", error);
    }
  };

  const eliminarJugador = async () => {
    if (!jugadorNombreBuscado) return alert("Ingresa un nombre válido");
    try {
      const res = await fetch(
        `https://aplicacion-web-m5oa.onrender.com/jugadores/${encodeURIComponent(jugadorNombreBuscado)}`,
        { method: "DELETE" }
      );
      if (res.ok) {
        alert("Jugador eliminado");
        setModo("listar");
      } else {
        alert("Error al eliminar jugador");
      }
    } catch (error) {
      console.error("Error eliminando jugador:", error);
    }
  };

  const manejarSubidaImagen = async (file: File) => {
    const url = await subirImagen(file);
    if (url) {
      setJugador((prev) => ({ ...prev, foto: url }));
    } else {
      alert("Error al subir imagen");
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      {/* Menú */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
          <div key={m} className="flex justify-center">
            <button
              className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 ${
                modo === m ? "bg-azul text-blanco border-azul" : "bg-blanco text-azul border-azul"
              }`}
              onClick={() => {
                setModo(m as any);
                setJugador({
                  nombre: "",
                  posicion: "",
                  fecha_nacimiento: "",
                  foto: "",
                  biografia: "",
                  dorsal: null,
                  id_equipo: 0,
                });
                setJugadorNombreBuscado("");
              }}
            >
              {m.toUpperCase()}
            </button>
          </div>
        ))}
      </div>

      {/* Input para nombre jugador */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="Nombre del jugador"
          value={jugadorNombreBuscado}
          onChange={(e) => setJugadorNombreBuscado(e.target.value)}
          className="rounded-[1rem] w-[90%] border px-3 py-2"
        />
      )}

      {/* Botón cargar jugador */}
      {(modo === "editar" || modo === "buscar") && (
        <div className="flex justify-center">
          <button
            onClick={obtenerJugador}
            className="px-4 py-2 rounded-full border-2 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            {modo === "buscar" ? "Buscar Jugador" : "Cargar Jugador"}
          </button>
        </div>
      )}

      {/* Resultado de búsqueda */}
      {modo === "buscar" && jugador.nombre && (
        <div className="mt-6 p-4 bg-blanco text-negro rounded-[1rem] shadow-md space-y-2">
          <p><strong>Nombre:</strong> {jugador.nombre}</p>
          <p><strong>Posición:</strong> {jugador.posicion}</p>
          <p><strong>Fecha de nacimiento:</strong> {jugador.fecha_nacimiento}</p>
          <p><strong>Dorsal:</strong> {jugador.dorsal}</p>
          <p><strong>ID Equipo:</strong> {jugador.id_equipo}</p>
          <p><strong>Biografía:</strong> {jugador.biografia}</p>
          {jugador.foto && (
            <img
              src={jugador.foto}
              alt={`Foto de ${jugador.nombre}`}
              className="w-24 h-24 rounded-xl mt-4 object-cover"
            />
          )}
        </div>
      )}

      {/* Crear o editar formulario */}
      {(modo === "crear" || (modo === "editar" && jugador.nombre)) && (
        <div className="space-y-2 max-w-md mt-2">
          {[
            { label: "Nombre", key: "nombre", type: "text" },
            { label: "Posición", key: "posicion", type: "select" },
            { label: "Fecha de nacimiento dd/mm/aaaa", key: "fecha_nacimiento", type: "date" },
            { label: "Biografía", key: "biografia", type: "text" },
            { label: "Dorsal", key: "dorsal", type: "number" },
            { label: "ID Equipo", key: "id_equipo", type: "select" },
          ].map(({ label, key, type }) => {
            if (key === "posicion") {
              return (
                <select
                  key={key}
                  value={jugador.posicion}
                  onChange={(e) =>
                    setJugador((prev) => ({ ...prev, posicion: e.target.value }))
                  }
                  className="rounded-[1rem] w-[95%] border px-3 py-2"
                >
                  <option value="" disabled>Selecciona posición</option>
                  <option value="Portero">Portero</option>
                  <option value="Defensa">Defensa</option>
                  <option value="Centrocampista">Centrocampista</option>
                  <option value="Delantero">Delantero</option>
                </select>
              );
            }

            if (key === "id_equipo") {
              return (
                <select
                  key={key}
                  value={jugador.id_equipo || ""}
                  onChange={(e) =>
                    setJugador((prev) => ({ ...prev, id_equipo: Number(e.target.value) }))
                  }
                  className="rounded-[1rem] w-[95%] border px-3 py-2"
                >
                  <option value="" disabled>Selecciona equipo</option>
                  <option value={1}>Masculino</option>
                  <option value={2}>Femenino</option>
                </select>
              );
            }

            if (key === "fecha_nacimiento") {
              return (
                <input
                  key={key}
                  type={isDate ? "date" : "text"}
                  placeholder={label}
                  value={jugador.fecha_nacimiento ?? ""}
                  onFocus={() => setIsDate(true)}
                  onBlur={() => setIsDate(false)}
                  onChange={(e) =>
                    setJugador((prev) => ({ ...prev, fecha_nacimiento: e.target.value }))
                  }
                  className="rounded-[1rem] w-[90%] border px-3 py-2"
                />
              );
            }

            return (
              <input
                key={key}
                type={type}
                placeholder={label}
                value={
                  key === "dorsal"
                    ? jugador.dorsal != null
                      ? jugador.dorsal.toString()
                      : ""
                    : (jugador[key as keyof Jugador] ?? "")
                }
                onChange={(e) => {
                  const val = type === "number" ? Number(e.target.value) : e.target.value;
                  setJugador((prev) => ({
                    ...prev,
                    [key]: val,
                  }));
                }}
                className="rounded-[1rem] w-[90%] border px-3 py-2"
              />
            );
          })}

          {/* Input de archivo */}
          <div className="space-y-1">
            <label>Foto del jugador</label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) manejarSubidaImagen(file);
              }}
              className="block w-[90%] text-sm"
            />
            {imagenCargando && <p className="text-yellow-400">Subiendo imagen...</p>}
            {errorImagen && <p className="text-red-600">{errorImagen}</p>}
            {jugador.foto && (
              <img
                src={jugador.foto}
                alt="Foto subida"
                className="w-24 h-24 mt-2 object-cover rounded-xl"
              />
            )}
          </div>

          <div className="flex justify-center">
            <button
              onClick={modo === "crear" ? crearJugador : actualizarJugador}
              className="px-4 py-2 rounded-full border-2 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco mt-4"
            >
              {modo === "crear" ? "Crear Jugador" : "Actualizar Jugador"}
            </button>
          </div>
        </div>
      )}

      {/* Listado de jugadores */}
      {modo === "listar" && (
        <div className="space-y-4">
          {jugadores.map((j) => (
            <div
              key={j.id_jugador ?? j.nombre}
              className="p-4 bg-blanco text-negro rounded-[1rem] shadow-md flex items-center gap-4"
            >
              {j.foto && (
                <img
                  src={j.foto}
                  alt={j.nombre}
                  className="w-12 h-12 object-cover rounded-xl"
                />
              )}
              <div>
                <p><strong>{j.nombre}</strong></p>
                <p>{j.posicion}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Botón eliminar */}
      {modo === "eliminar" && jugadorNombreBuscado && (
        <div className="flex justify-center mt-4">
          <button
            onClick={eliminarJugador}
            className="px-4 py-2 rounded-full border-2 bg-red-600 text-blanco border-red-600 hover:bg-red-700"
          >
            Eliminar Jugador
          </button>
        </div>
      )}
    </div>
  );
}

