import { useState, useEffect } from "react";

interface Patrocinador {
  nombre: string;
  tipo: string;
  email: string;
  telefono: string;
  logo: string;
  fecha_inicio: string; // formato YYYY-MM-DD
  fecha_fin: string;    // formato YYYY-MM-DD
  dni_administrador: string;
}

export default function Patrocinadores() {
  const [modo, setModo] = useState<
    "crear" | "listar" | "buscar" | "editar" | "eliminar"
  >("listar");

  const [nombreBuscado, setNombreBuscado] = useState("");
  const [patrocinador, setPatrocinador] = useState<Patrocinador>({
    nombre: "",
    tipo: "",
    email: "",
    telefono: "",
    logo: "",
    fecha_inicio: "",
    fecha_fin: "",
    dni_administrador: "",
  });

  const [patrocinadores, setPatrocinadores] = useState<Patrocinador[]>([]);

  useEffect(() => {
    if (modo === "listar") {
      fetch("http://localhost:8000/patrocinadores/")
        .then((res) => res.json())
        .then(setPatrocinadores)
        .catch((e) => console.error("Error listando patrocinadores:", e));
    }
  }, [modo]);

  const obtenerPatrocinador = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/patrocinadores/${encodeURIComponent(nombreBuscado)}`
      );
      if (res.ok) {
        const data = await res.json();
        setPatrocinador({ ...data, dni_administrador: "" });
      } else {
        alert("Patrocinador no encontrado");
      }
    } catch (error) {
      console.error("Error al obtener patrocinador:", error);
    }
  };

  const crearPatrocinador = async () => {
    try {
      const res = await fetch("http://localhost:8000/patrocinadores/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patrocinador),
      });
      if (res.ok) {
        alert("Patrocinador creado");
        setPatrocinador({
          nombre: "",
          tipo: "",
          email: "",
          telefono: "",
          logo: "",
          fecha_inicio: "",
          fecha_fin: "",
          dni_administrador: "",
        });
        setModo("listar");
      } else {
        alert("Error al crear patrocinador");
      }
    } catch (error) {
      console.error("Error creando patrocinador:", error);
    }
  };

  const actualizarPatrocinador = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/patrocinadores/${encodeURIComponent(nombreBuscado)}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(patrocinador),
        }
      );
      if (res.ok) {
        alert("Patrocinador actualizado");
      } else {
        alert("Error al actualizar patrocinador");
      }
    } catch (error) {
      console.error("Error actualizando patrocinador:", error);
    }
  };

  const eliminarPatrocinador = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/patrocinadores/${encodeURIComponent(nombreBuscado)}`,
        {
          method: "DELETE",
        }
      );
      if (res.ok) {
        alert("Patrocinador eliminado");
        setModo("listar");
      } else {
        alert("Error al eliminar patrocinador");
      }
    } catch (error) {
      console.error("Error eliminando patrocinador:", error);
    }
  };

  return (
    <div className="p-4 space-y-4">
      {/* Menú de opciones */}
      <div className="flex flex-wrap gap-2">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
          <button
            key={m}
            className={`px-3 py-1 rounded border ${
              modo === m ? "bg-blue-600 text-white" : "bg-white text-black"
            }`}
            onClick={() => {
              setModo(m as any);
              setPatrocinador({
                nombre: "",
                tipo: "",
                email: "",
                telefono: "",
                logo: "",
                fecha_inicio: "",
                fecha_fin: "",
                dni_administrador: "",
              });
              setNombreBuscado("");
            }}
          >
            {m.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Input para nombre buscado */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="Nombre del patrocinador"
          value={nombreBuscado}
          onChange={(e) => setNombreBuscado(e.target.value)}
          className="border p-2 rounded w-full"
        />
      )}

      {/* Buscar patrocinador */}
      {modo === "buscar" && (
        <>
          <button
            onClick={obtenerPatrocinador}
            className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
          >
            Obtener Patrocinador
          </button>
          {patrocinador.nombre && (
            <div className="mt-4 border p-4 rounded shadow">
              <h3 className="font-bold text-xl mb-2">{patrocinador.nombre}</h3>
              <img
                src={patrocinador.logo}
                alt={patrocinador.nombre}
                className="w-full h-48 object-contain mb-2"
              />
              <p><b>Tipo:</b> {patrocinador.tipo}</p>
              <p><b>Email:</b> {patrocinador.email}</p>
              <p><b>Teléfono:</b> {patrocinador.telefono}</p>
              <p><b>Fecha Inicio:</b> {patrocinador.fecha_inicio}</p>
              <p><b>Fecha Fin:</b> {patrocinador.fecha_fin}</p>
            </div>
          )}
        </>
      )}

      {/* Crear patrocinador */}
      {modo === "crear" && (
        <div className="space-y-2 max-w-md">
          {[
            { label: "Nombre", key: "nombre", type: "text" },
            { label: "Tipo", key: "tipo", type: "text" },
            { label: "Email", key: "email", type: "email" },
            { label: "Teléfono", key: "telefono", type: "text" },
            { label: "Logo (URL)", key: "logo", type: "text" },
            { label: "Fecha Inicio", key: "fecha_inicio", type: "date" },
            { label: "Fecha Fin", key: "fecha_fin", type: "date" },
            { label: "DNI Administrador", key: "dni_administrador", type: "text" },
          ].map(({ label, key, type }) => (
            <input
              key={key}
              type={type}
              placeholder={label}
              value={patrocinador[key as keyof Patrocinador]}
              onChange={(e) =>
                setPatrocinador((prev) => ({
                  ...prev,
                  [key]: e.target.value,
                }))
              }
              className="border p-2 rounded w-full"
            />
          ))}
          <button
            onClick={crearPatrocinador}
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Crear Patrocinador
          </button>
        </div>
      )}

      {/* Editar patrocinador */}
      {modo === "editar" && (
        <>
          <button
            onClick={obtenerPatrocinador}
            className="bg-yellow-400 text-white px-4 py-2 rounded"
          >
            Cargar Patrocinador
          </button>
          {patrocinador.nombre && (
            <div className="space-y-2 max-w-md mt-2">
              {[
                { label: "Nombre", key: "nombre", type: "text" },
                { label: "Tipo", key: "tipo", type: "text" },
                { label: "Email", key: "email", type: "email" },
                { label: "Teléfono", key: "telefono", type: "text" },
                { label: "Logo (URL)", key: "logo", type: "text" },
                { label: "Fecha Inicio", key: "fecha_inicio", type: "date" },
                { label: "Fecha Fin", key: "fecha_fin", type: "date" },
                { label: "DNI Administrador", key: "dni_administrador", type: "text" },
              ].map(({ label, key, type }) => (
                <input
                  key={key}
                  type={type}
                  placeholder={label}
                  value={patrocinador[key as keyof Patrocinador]}
                  onChange={(e) =>
                    setPatrocinador((prev) => ({
                      ...prev,
                      [key]: e.target.value,
                    }))
                  }
                  className="border p-2 rounded w-full"
                />
              ))}
              <button
                onClick={actualizarPatrocinador}
                className="bg-green-500 text-white px-4 py-2 rounded"
              >
                Guardar Cambios
              </button>
            </div>
          )}
        </>
      )}

      {/* Eliminar patrocinador */}
      {modo === "eliminar" && (
        <>
          <button
            onClick={eliminarPatrocinador}
            disabled={!nombreBuscado}
            className="bg-red-600 text-white px-4 py-2 rounded"
          >
            Eliminar Patrocinador
          </button>
        </>
      )}

      {/* Listar patrocinadores */}
      {modo === "listar" && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {patrocinadores.map((p) => (
            <div
              key={p.nombre}
              className="border rounded p-4 shadow hover:shadow-lg transition"
            >
              <h3 className="font-bold text-lg">{p.nombre}</h3>
              <img
                src={p.logo}
                alt={p.nombre}
                className="w-full h-32 object-contain my-2"
              />
              <p><b>Tipo:</b> {p.tipo}</p>
              <p><b>Email:</b> {p.email}</p>
              <p><b>Teléfono:</b> {p.telefono}</p>
              <p><b>Inicio:</b> {p.fecha_inicio}</p>
              <p><b>Fin:</b> {p.fecha_fin}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

