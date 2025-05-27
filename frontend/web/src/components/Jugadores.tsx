import { useState, useEffect } from "react";

interface Jugador {
  nombre: string;
  posicion: string;
  fecha_nacimiento: string; // YYYY-MM-DD
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

  const [jugadorIdBuscado, setJugadorIdBuscado] = useState<string>("");

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

  useEffect(() => {
    if (modo === "listar") {
      fetch("http://localhost:8000/jugadores/")
        .then((res) => res.json())
        .then(setJugadores)
        .catch((e) => console.error("Error listando jugadores:", e));
    }
  }, [modo]);

  const obtenerJugador = async () => {
    if (!jugadorIdBuscado) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(
        `http://localhost:8000/jugadores/${encodeURIComponent(jugadorIdBuscado)}`
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
      const res = await fetch("http://localhost:8000/jugadores/", {
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
    if (!jugadorIdBuscado) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(
        `http://localhost:8000/jugadores/${encodeURIComponent(jugadorIdBuscado)}`,
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
    if (!jugadorIdBuscado) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(
        `http://localhost:8000/jugadores/${encodeURIComponent(jugadorIdBuscado)}`,
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

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      {/* Menú */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
        <div className="flex justify-center"> 
          <button
            key={m}
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco ${
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
              setJugadorIdBuscado("");
            }}
          >
            {m.toUpperCase()}
          </button>
          </div>
        ))}
      </div>

      {/* Input para ID jugador en modos buscar, editar, eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="number"
          placeholder="ID del jugador"
          value={jugadorIdBuscado}
          onChange={(e) => setJugadorIdBuscado(e.target.value)}
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
        />
      )}

      {/* Botón para obtener jugador (buscar, editar) */}
     {(modo === "editar") && (
  <>
    <div className="flex justify-center"> 
      <button
        onClick={obtenerJugador}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
      >
        Cargar Jugador
      </button>
    </div>

    </>
)}
	     {(modo === "buscar") && (
  <>
    <div className="flex justify-center"> 
      <button
        onClick={obtenerJugador}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
      >
        Buscar Jugador
      </button>
    </div>

    {jugador && (
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
  </>
)}

      {/* Formulario para crear */}
      {modo === "crear" && (
        <div className="space-y-2 max-w-md">
          {[
            { label: "Nombre", key: "nombre", type: "text" },
            { label: "Posición", key: "posicion", type: "text" },
            { label: "Fecha de nacimiento", key: "fecha_nacimiento", type: "date" },
            { label: "Foto (URL)", key: "foto", type: "text" },
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
              className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
            />
          ))}
          <div className="flex justify-center"> 
          <button
            onClick={crearJugador}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Crear Jugador
          </button>
          </div>
        </div>
      )}

      {/* Formulario para editar */}
      {modo === "editar" && jugador.id_jugador && (
        <div className="space-y-2 max-w-md mt-2">
          {[
            { label: "Nombre", key: "nombre", type: "text" },
            { label: "Posición", key: "posicion", type: "text" },
            { label: "Fecha de nacimiento", key: "fecha_nacimiento", type: "date" },
            { label: "Foto (URL)", key: "foto", type: "text" },
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
              className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
            />
          ))}
          <div className="flex justify-center"> 
          <button
            onClick={actualizarJugador}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Guardar Cambios
          </button>
          </div>

        </div>
      )}

      {/* Botón eliminar */}
      {modo === "eliminar" && (
      <div className="flex justify-center"> 
        <button
          onClick={eliminarJugador}
          disabled={!jugadorIdBuscado}
          className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
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
              key={j.id_jugador}
              className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4"
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

