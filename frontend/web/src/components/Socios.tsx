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
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4     div superior">
      {/* Menú de modos */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
        <div className="flex justify-center"> 
          <button
            key={m}
            onClick={() => {
              setModo(m as any);
              setSocio(null);
              setDni("");
            }}
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco ${
              modo === m ? "bg-blue-500 text-white" : "bg-white text-black"
            }`}
          >
            {m.toUpperCase()}
          </button>
          </div>
        ))}
      </div>

      {/* Input DNI para buscar/editar/eliminar */}
      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="DNI"
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          value={dni}
          onChange={(e) => setDni(e.target.value)}
        />
      )}

      {modo === "buscar" && (
  <>
    <div className="flex justify-center"> 
      <button onClick={obtenerSocio} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
        Obtener Socio
      </button>
    </div>
    {socio && (
      <div className="mt-6 p-4 bg-blanco text-negro rounded-[1rem] shadow-md space-y-2">
        <p><strong>DNI:</strong> {socio.dni}</p>
        <p><strong>Número Socio:</strong> {socio.num_socio}</p>
        <p><strong>Membresía:</strong> {socio.tipo_membresia}</p>
        <p><strong>Estado:</strong> {socio.estado}</p>
        {socio.foto_perfil && (
          <img
            src={socio.foto_perfil}
            alt="Foto de perfil"
            className="w-24 h-24 rounded-full mt-4"
          />
        )}
      </div>
    )}
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
              className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
              value={(socio as any)?.[campo] || ""}
              onChange={(e) =>
                setSocio((prev) => ({ ...prev, [campo]: e.target.value }))
              }
            />
          ))}
          <div className="flex justify-center"> 
          <button onClick={crearSocio} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
            Crear Socio
          </button>
          </div>
        </div>
      )}

      {/* Editar socio */}
      {modo === "editar" && (
        <>
        <div className="flex justify-center"> 
          <button onClick={obtenerSocio} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
            Cargar Socio
          </button>
          </div>
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
                  className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              ))}
              <div className="flex justify-center"> 
              <button onClick={actualizarSocio} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
                Guardar Cambios
              </button>
              </div>
            </div>
          )}
        </>
      )}

      {/* Eliminar socio */}
      {modo === "eliminar" && (
      <div className="flex justify-center"> 
        <button onClick={eliminarSocio} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
          Eliminar Socio
        </button>
        </div>
      )}

      {/* Listar socios */}
      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {socios.map((s) => (
            <div key={s.dni} className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4">
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

