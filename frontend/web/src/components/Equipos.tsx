import { useState, useEffect } from "react";

interface Equipo {
  categoria: string;
  num_jugadores: number;
  id_equipo?: number;
}

export default function Equipos() {
  const [modo, setModo] = useState<
    "crear" | "listar" | "buscar" | "editar" | "eliminar"
  >("listar");

  const [equipoIdBuscado, setEquipoIdBuscado] = useState<string>("");

  const [equipo, setEquipo] = useState<Equipo>({
    categoria: "",
    num_jugadores: 0,
  });

  const [equipos, setEquipos] = useState<Equipo[]>([]);

  useEffect(() => {
    if (modo === "listar") {
      fetch("http://localhost:8000/equipos/")
        .then((res) => res.json())
        .then(setEquipos)
        .catch((e) => console.error("Error listando equipos:", e));
    }
  }, [modo]);

  const obtenerEquipo = async () => {
    if (!equipoIdBuscado) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(
        `http://localhost:8000/equipos/${encodeURIComponent(equipoIdBuscado)}`
      );
      if (res.ok) {
        const data = await res.json();
        setEquipo(data);
      } else {
        alert("Equipo no encontrado");
      }
    } catch (error) {
      console.error("Error obteniendo equipo:", error);
    }
  };

  const crearEquipo = async () => {
    try {
      const res = await fetch("http://localhost:8000/equipos/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(equipo),
      });
      if (res.ok) {
        alert("Equipo creado");
        setEquipo({ categoria: "", num_jugadores: 0 });
        setModo("listar");
      } else {
        alert("Error al crear equipo");
      }
    } catch (error) {
      console.error("Error creando equipo:", error);
    }
  };

  const actualizarEquipo = async () => {
    if (!equipoIdBuscado) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(
        `http://localhost:8000/equipos/${encodeURIComponent(equipoIdBuscado)}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(equipo),
        }
      );
      if (res.ok) {
        alert("Equipo actualizado");
      } else {
        alert("Error al actualizar equipo");
      }
    } catch (error) {
      console.error("Error actualizando equipo:", error);
    }
  };

  const eliminarEquipo = async () => {
    if (!equipoIdBuscado) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(
        `http://localhost:8000/equipos/${encodeURIComponent(equipoIdBuscado)}`,
        { method: "DELETE" }
      );
      if (res.ok) {
        alert("Equipo eliminado");
        setModo("listar");
      } else {
        alert("Error al eliminar equipo");
      }
    } catch (error) {
      console.error("Error eliminando equipo:", error);
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4 ">
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
              setEquipo({ categoria: "", num_jugadores: 0 });
              setEquipoIdBuscado("");
            }}
          >
            {m.toUpperCase()}
          </button>
          </div>
        ))}
      </div>

      {/* Input para ID equipo en buscar, editar, eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="number"
          placeholder="ID del equipo"
          value={equipoIdBuscado}
          onChange={(e) => setEquipoIdBuscado(e.target.value)}
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
        />
      )}

      {/* Botón cargar equipo */}
      {modo === "buscar" && (
  <>
    <div className="flex justify-center">
      <button
        onClick={obtenerEquipo}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
      >
        Buscar Equipo
      </button>
    </div>

    {equipo && (
      <div className="mt-6 p-4 bg-blanco text-negro rounded-[1rem] shadow-md space-y-2">
        <p><strong>Categoría:</strong> {equipo.categoria}</p>
        <p><strong>Número de jugadores:</strong> {equipo.num_jugadores}</p>
        <p><strong>ID Equipo:</strong> {equipo.id_equipo}</p>
      </div>
    )}
  </>
)}


      {/* Formulario crear */}
      {modo === "crear" && (
        <div className="space-y-2 max-w-md">
          <input
            type="text"
            placeholder="Categoría"
            value={equipo.categoria}
            onChange={(e) =>
              setEquipo((prev) => ({ ...prev, categoria: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="number"
            placeholder="Número de jugadores"
            value={equipo.num_jugadores}
            onChange={(e) =>
              setEquipo((prev) => ({ ...prev, num_jugadores: Number(e.target.value) }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          />
          <div className="flex justify-center">
          <button
            onClick={crearEquipo}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Crear Equipo
          </button>
          </div>
        </div>
      )}

      {/* Formulario editar */}
      {modo === "editar" && equipo.id_equipo && (
        <div className="space-y-2 max-w-md mt-2">
          <input
            type="text"
            placeholder="Categoría"
            value={equipo.categoria}
            onChange={(e) =>
              setEquipo((prev) => ({ ...prev, categoria: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="number"
            placeholder="Número de jugadores"
            value={equipo.num_jugadores}
            onChange={(e) =>
              setEquipo((prev) => ({ ...prev, num_jugadores: Number(e.target.value) }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <div className="flex justify-center">
          <button
            onClick={actualizarEquipo}
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
          onClick={eliminarEquipo}
          disabled={!equipoIdBuscado}
          className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Eliminar Equipo
        </button>
        </div>
      )}

      {/* Listado */}
      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {equipos.map((e) => (
            <div
              key={e.id_equipo}
              className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4"
            >
              <h3 className="font-bold text-lg">Categoría: {e.categoria}</h3>
              <p><b>Número de jugadores:</b> {e.num_jugadores}</p>
              <p><b>ID Equipo:</b> {e.id_equipo}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

