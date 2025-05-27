import { useEffect, useState } from "react";

interface Socio {
  dni: string;
  num_socio: string;
  tipo_membresia: string;
  estado: string;
  foto_perfil: string;
  nombre?: string;
  apellidos?: string;
  telefono?: string;
  fecha_nacimiento?: string;
  email?: string;
  contrasena?: string;
  tipo_socio?: string;
}

export default function Socios() {
  const [modo, setModo] = useState<"crear" | "listar" | "buscar" | "editar" | "eliminar">("listar");
  const [dni, setDni] = useState("");
  const [socio, setSocio] = useState<Socio | null>(null);
  const [socios, setSocios] = useState<Socio[]>([]);

  useEffect(() => {
    if (modo === "listar") {
      fetch("http://localhost:8000/socios/")
        .then((res) => res.json())
        .then(setSocios)
        .catch((err) => console.error("Error al listar socios:", err));
    }
  }, [modo]);

  const obtenerSocio = async () => {
    try {
      const res = await fetch(`http://localhost:8000/socios/${dni}`);
      if (res.ok) {
        const data = await res.json();
        setSocio(data);
      } else {
        alert("Socio no encontrado.");
      }
    } catch (err) {
      console.error("Error al obtener socio:", err);
    }
  };

  const crearSocio = async () => {
    try {
      const res = await fetch(`http://localhost:8000/socios/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(socio),
      });
      if (res.ok) {
        alert("Socio creado correctamente.");
        setSocio(null);
        setModo("listar");
      } else {
        alert("Error al crear socio.");
      }
    } catch (err) {
      console.error("Error al crear socio:", err);
    }
  };

  const actualizarSocio = async () => {
    try {
      const res = await fetch(`http://localhost:8000/socios/${dni}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tipo_membresia: socio?.tipo_membresia,
          estado: socio?.estado,
          foto_perfil: socio?.foto_perfil,
        }),
      });
      if (res.ok) {
        alert("Socio actualizado.");
      } else {
        alert("Error al actualizar socio.");
      }
    } catch (err) {
      console.error("Error al actualizar socio:", err);
    }
  };

  const eliminarSocio = async () => {
    try {
      const res = await fetch(`http://localhost:8000/socios/${dni}`, {
        method: "DELETE",
      });
      if (res.ok) {
        alert("Socio eliminado.");
        setModo("listar");
      } else {
        alert("Error al eliminar socio.");
      }
    } catch (err) {
      console.error("Error al eliminar socio:", err);
    }
  };

  const camposCrear = [
    "dni",
    "num_socio",
    "tipo_membresia",
    "estado",
    "foto_perfil",
    "nombre",
    "apellidos",
    "telefono",
    "fecha_nacimiento",
    "email",
    "contrasena",
    "tipo_socio",
  ];

  return (
    <div className="p-4 space-y-4">
      {/* Menú de modos */}
      <div className="flex flex-wrap gap-2">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
          <button
            key={m}
            onClick={() => {
              setModo(m as any);
              setSocio(null);
              setDni("");
            }}
            className={`px-3 py-1 rounded border ${
              modo === m ? "bg-blue-500 text-white" : "bg-white text-black"
            }`}
          >
            {m.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Input DNI para buscar/editar/eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="DNI"
          className="border p-2 rounded w-full"
          value={dni}
          onChange={(e) => setDni(e.target.value)}
        />
      )}

      {/* Buscar socio */}
      {modo === "buscar" && (
        <>
          <button onClick={obtenerSocio} className="bg-blue-500 text-white px-4 py-2 rounded mt-2">
            Obtener Socio
          </button>
          {socio && <pre>{JSON.stringify(socio, null, 2)}</pre>}
        </>
      )}

      {/* Crear socio */}
      {modo === "crear" && (
        <div className="space-y-2">
          {camposCrear.map((campo) => (
            <input
              key={campo}
              type={campo === "fecha_nacimiento" ? "date" : "text"}
              placeholder={campo}
              className="border p-2 rounded w-full"
              value={(socio as any)?.[campo] || ""}
              onChange={(e) =>
                setSocio((prev) => ({ ...prev, [campo]: e.target.value }))
              }
            />
          ))}
          <button onClick={crearSocio} className="bg-green-600 text-white px-4 py-2 rounded">
            Crear Socio
          </button>
        </div>
      )}

      {/* Editar socio */}
      {modo === "editar" && (
        <>
          <button onClick={obtenerSocio} className="bg-yellow-400 text-white px-4 py-2 rounded">
            Cargar Socio
          </button>
          {socio && (
            <div className="space-y-2 mt-2">
              {["tipo_membresia", "estado", "foto_perfil"].map((campo) => (
                <input
                  key={campo}
                  type="text"
                  placeholder={campo}
                  value={(socio as any)[campo]}
                  onChange={(e) =>
                    setSocio((prev) => prev && { ...prev, [campo]: e.target.value })
                  }
                  className="border p-2 rounded w-full"
                />
              ))}
              <button onClick={actualizarSocio} className="bg-green-500 text-white px-4 py-2 rounded">
                Guardar Cambios
              </button>
            </div>
          )}
        </>
      )}

      {/* Eliminar socio */}
      {modo === "eliminar" && (
        <button onClick={eliminarSocio} className="bg-red-600 text-white px-4 py-2 rounded mt-2">
          Eliminar Socio
        </button>
      )}

      {/* Listar socios */}
      {modo === "listar" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-4">
          {socios.map((s) => (
            <div key={s.dni} className="p-3 border rounded shadow">
              <strong>{s.dni}</strong> - {s.num_socio}
              <div>Membresía: {s.tipo_membresia}</div>
              <div>Estado: {s.estado}</div>
              {s.foto_perfil && (
                <img src={s.foto_perfil} alt="Perfil" className="h-16 w-16 object-cover mt-1" />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

