import { useState, useEffect } from "react";
import { useSubirImagen } from "../hooks/useSubirImagen";

interface Jugador {
  nombre: string;
  posicion: string;
  fecha_nacimiento: string;
  foto: string;
  biografia: string;
  dorsal: number;
  id_equipo: number;
  id_jugador?: number;
}

export default function Jugadores() {
  const [modo, setModo] = useState<
    "crear" | "listar" | "buscar" | "editar" | "eliminar"
  >("listar");

  const [jugadorNombreBuscado, setJugadorNombreBuscado] = useState<string>("");

  const [jugador, setJugador] = useState<Jugador>({
    nombre: "",
    posicion: "",
    fecha_nacimiento: "",
    foto: "",
    biografia: "",
    dorsal: 0,
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
          dorsal: 0,
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
                modo === m ? "bg-blue-600 text-white" : "bg-white text-black"
              }`}
              onClick={() => {
                setModo(m as any);
                setJugador({
                  nombre: "",
                  posicion: "",
                  fecha_nacimiento: "",
                  foto: "",
                  biografia: "",
                  dorsal: 0,
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
            className="px-4 py-2 rounded-full border-2 bg-blanco text-azul hover:bg-azul hover:text-blanco"
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
            { label: "Posición", key: "posicion", type: "text" },
            { label: "Fecha de nacimiento", key: "fecha_nacimiento", type: "date" },
            { label: "Biografía", key: "biografia", type: "text" },
            { label: "Dorsal", key: "dorsal", type: "number" },
            { label: "ID Equipo", key: "id_equipo", type: "number" },
          ].map(({ label, key, type }) => (
            <input
              key={key}
              type={type}
              placeholder={label}
              value={
                key === "dorsal" || key === "id_equipo"
                  ? jugador[key as keyof Jugador]?.toString()
                  : jugador[key as keyof Jugador]
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
          ))}

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
              className="px-4 py-2 rounded-full border-2 bg-blanco text-azul hover:bg-azul hover:text-blanco"
            >
              {modo === "crear" ? "Crear Jugador" : "Guardar Cambios"}
            </button>
          </div>
        </div>
      )}

      {/* Botón eliminar */}
      {modo === "eliminar" && (
        <div className="flex justify-center">
          <button
            onClick={eliminarJugador}
            disabled={!jugadorNombreBuscado}
            className="px-4 py-2 rounded-full border-2 bg-blanco text-azul hover:bg-azul hover:text-blanco"
          >
            Eliminar Jugador
          </button>
        </div>
      )}

      {/* Listado */}
      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {jugadores.map((j) => (
            <div
              key={j.nombre}
              className="bg-blanco text-negro px-6 py-10 rounded-[1rem] shadow-lg space-y-4"
            >
              <h3 className="font-bold text-lg">{j.nombre}</h3>
              <img
                src={j.foto}
                alt={j.nombre}
                className="w-full h-32 object-contain my-2"
              />
              <p><b>Posición:</b> {j.posicion}</p>
              <p><b>Fecha Nac.:</b> {j.fecha_nacimiento}</p>
              <p><b>Dorsal:</b> {j.dorsal}</p>
              <p><b>ID Equipo:</b> {j.id_equipo}</p>
              <p className="text-sm mt-2">{j.biografia}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

