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
    <div className="p-4 space-y-4">
      {/* Menú */}
      <div className="flex flex-wrap gap-2">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
          <button
            key={m}
            className={`px-3 py-1 rounded border ${
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
        ))}
      </div>

      {/* Input para ID equipo en buscar, editar, eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="number"
          placeholder="ID del equipo"
          value={equipoIdBuscado}
          onChange={(e) => setEquipoIdBuscado(e.target.value)}
          className="border p-2 rounded w-full max-w-xs"
        />
      )}

      {/* Botón cargar equipo */}
      {(modo === "buscar" || modo === "editar") && (
        <button
          onClick={obtenerEquipo}
          className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
        >
          Cargar Equipo
        </button>
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
            className="border p-2 rounded w-full"
          />
          <input
            type="number"
            placeholder="Número de jugadores"
            value={equipo.num_jugadores}
            onChange={(e) =>
              setEquipo((prev) => ({ ...prev, num_jugadores: Number(e.target.value) }))
            }
            className="border p-2 rounded w-full"
          />
          <button
            onClick={crearEquipo}
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Crear Equipo
          </button>
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
            className="border p-2 rounded w-full"
          />
          <input
            type="number"
            placeholder="Número de jugadores"
            value={equipo.num_jugadores}
            onChange={(e) =>
              setEquipo((prev) => ({ ...prev, num_jugadores: Number(e.target.value) }))
            }
            className="border p-2 rounded w-full"
          />
          <button
            onClick={actualizarEquipo}
            className="bg-green-500 text-white px-4 py-2 rounded"
          >
            Guardar Cambios
          </button>
        </div>
      )}

      {/* Botón eliminar */}
      {modo === "eliminar" && (
        <button
          onClick={eliminarEquipo}
          disabled={!equipoIdBuscado}
          className="bg-red-600 text-white px-4 py-2 rounded"
        >
          Eliminar Equipo
        </button>
      )}

      {/* Listado */}
      {modo === "listar" && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {equipos.map((e) => (
            <div
              key={e.id_equipo}
              className="border rounded p-4 shadow hover:shadow-lg transition"
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

