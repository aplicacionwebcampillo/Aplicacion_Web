import { useState, useEffect } from "react";

interface Abono {
  temporada: string;
  precio: number;
  fecha_inicio: string; // formato "YYYY-MM-DD"
  fecha_fin: string;
  descripcion: string;
  id_abono?: number;
}

export default function Abonos() {
  const [modo, setModo] = useState<
    "crear" | "listar" | "buscar" | "editar" | "eliminar"
  >("listar");

  const [abonoIdBuscado, setAbonoIdBuscado] = useState<string>("");

  const [abono, setAbono] = useState<Abono>({
    temporada: "",
    precio: 0,
    fecha_inicio: "",
    fecha_fin: "",
    descripcion: "",
  });

  const [abonos, setAbonos] = useState<Abono[]>([]);

  useEffect(() => {
    if (modo === "listar") {
      fetch("http://localhost:8000/abonos/")
        .then((res) => res.json())
        .then(setAbonos)
        .catch((e) => console.error("Error listando abonos:", e));
    }
  }, [modo]);

  const obtenerAbono = async () => {
    if (!abonoIdBuscado) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(
        `http://localhost:8000/abonos/${encodeURIComponent(abonoIdBuscado)}`
      );
      if (res.ok) {
        const data = await res.json();
        setAbono(data);
      } else {
        alert("Abono no encontrado");
      }
    } catch (error) {
      console.error("Error obteniendo abono:", error);
    }
  };

  const crearAbono = async () => {
    try {
      const res = await fetch("http://localhost:8000/abonos/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(abono),
      });
      if (res.ok) {
        alert("Abono creado");
        setAbono({
          temporada: "",
          precio: 0,
          fecha_inicio: "",
          fecha_fin: "",
          descripcion: "",
        });
        setModo("listar");
      } else {
        alert("Error al crear abono");
      }
    } catch (error) {
      console.error("Error creando abono:", error);
    }
  };

  const actualizarAbono = async () => {
    if (!abonoIdBuscado) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(
        `http://localhost:8000/abonos/${encodeURIComponent(abonoIdBuscado)}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(abono),
        }
      );
      if (res.ok) {
        alert("Abono actualizado");
      } else {
        alert("Error al actualizar abono");
      }
    } catch (error) {
      console.error("Error actualizando abono:", error);
    }
  };

  const eliminarAbono = async () => {
    if (!abonoIdBuscado) return alert("Ingresa un ID válido");
    try {
      const res = await fetch(
        `http://localhost:8000/abonos/${encodeURIComponent(abonoIdBuscado)}`,
        { method: "DELETE" }
      );
      if (res.ok) {
        alert("Abono eliminado");
        setModo("listar");
      } else {
        alert("Error al eliminar abono");
      }
    } catch (error) {
      console.error("Error eliminando abono:", error);
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4   ">
      {/* Menú */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
        <div className="flex justify-center"> 
          <button
            key={m}
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco ${
              modo === m ? "bg-blue-600 text-white" : "bg-white text-black"
            }`}
            onClick={() => {
              setModo(m as any);
              setAbono({
                temporada: "",
                precio: 0,
                fecha_inicio: "",
                fecha_fin: "",
                descripcion: "",
              });
              setAbonoIdBuscado("");
            }}
          >
            {m.toUpperCase()}
          </button>
          </div>
        ))}
      </div>

      {/* Input para ID abono en buscar, editar, eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="number"
          placeholder="ID del abono"
          value={abonoIdBuscado}
          onChange={(e) => setAbonoIdBuscado(e.target.value)}
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
        />
      )}

      {/* Botón cargar abono */}
      {(modo === "editar") && (
      <div className="flex justify-center"> 
        <button
          onClick={obtenerAbono}
          className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Cargar Abono
        </button>
        </div>
      )}
      
      {modo === "buscar" && (
  <>
    <div className="flex justify-center">
      <button
        onClick={obtenerAbono}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
      >
        Buscar Abono
      </button>
    </div>

    {abono && (
      <div className="mt-6 p-4 bg-blanco text-negro rounded-[1rem] shadow-md space-y-2">
        <h3 className="font-bold text-lg">Temporada: {abono.temporada}</h3>
              <p><b>Precio:</b> {abono.precio}€</p>
              <p>
                <b>Desde:</b> {abono.fecha_inicio} <b>Hasta:</b> {abono.fecha_fin}
              </p>
              <p>{abono.descripcion}</p>
              <p><b>ID Abono:</b> {abono.id_abono}</p>
      </div>
    )}
  </>
)}


      {/* Formulario crear */}
      {modo === "crear" && (
        <div className="space-y-2 max-w-md">
          <input
            type="text"
            placeholder="Temporada"
            value={abono.temporada}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, temporada: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
          />
          <input
            type="number"
            placeholder="Precio"
            value={abono.precio}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, precio: Number(e.target.value) }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
          />
          <input
            type="date"
            placeholder="Fecha Inicio"
            value={abono.fecha_inicio}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, fecha_inicio: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
          />
          <input
            type="date"
            placeholder="Fecha Fin"
            value={abono.fecha_fin}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, fecha_fin: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
          />
          <textarea
            placeholder="Descripción"
            value={abono.descripcion}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, descripcion: e.target.value }))
            }
            className="border p-2 rounded w-full"
            rows={3}
          />
          <div className="flex justify-center"> 
          <button
            onClick={crearAbono}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
          >
            Crear Abono
          </button>
          </div>
        </div>
      )}

      {/* Formulario editar */}
      {modo === "editar" && abono.id_abono && (
        <div className="space-y-2 max-w-md mt-2">
          <input
            type="text"
            placeholder="Temporada"
            value={abono.temporada}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, temporada: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
          />
          <input
            type="number"
            placeholder="Precio"
            value={abono.precio}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, precio: Number(e.target.value) }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
          />
          <input
            type="date"
            placeholder="Fecha Inicio"
            value={abono.fecha_inicio}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, fecha_inicio: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
          />
          <input
            type="date"
            placeholder="Fecha Fin"
            value={abono.fecha_fin}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, fecha_fin: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
          />
          <textarea
            placeholder="Descripción"
            value={abono.descripcion}
            onChange={(e) =>
              setAbono((prev) => ({ ...prev, descripcion: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500  "
            rows={3}
          />
          <div className="flex justify-center"> 
          <button
            onClick={actualizarAbono}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
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
          onClick={eliminarAbono}
          disabled={!abonoIdBuscado}
          className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Eliminar Abono
        </button>
        </div>
      )}

      {/* Listado */}
      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {abonos.map((a) => (
            <div
              key={a.id_abono}
              className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4"
            >
              <h3 className="font-bold text-lg">Temporada: {a.temporada}</h3>
              <p><b>Precio:</b> {a.precio}€</p>
              <p>
                <b>Desde:</b> {a.fecha_inicio} <b>Hasta:</b> {a.fecha_fin}
              </p>
              <p>{a.descripcion}</p>
              <p><b>ID Abono:</b> {a.id_abono}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

