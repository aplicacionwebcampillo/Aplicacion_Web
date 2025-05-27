import { useEffect, useState } from "react";

interface Administrador {
  dni: string;
  cargo: string;
  permisos: string;
  estado: string;
  foto_perfil: string;
  nombre?: string;
  apellidos?: string;
  telefono?: string;
  fecha_nacimiento?: string;
  email?: string;
  contrasena?: string;
}

export default function Administrador() {
  const [modo, setModo] = useState<"crear" | "listar" | "buscar" | "editar" | "eliminar">("listar");
  const [dni, setDni] = useState("");
  const [admin, setAdmin] = useState<Administrador | null>(null);
  const [admins, setAdmins] = useState<Administrador[]>([]);

  useEffect(() => {
    if (modo === "listar") {
      fetch("http://localhost:8000/administradores/")
        .then((res) => res.json())
        .then(setAdmins)
        .catch((err) => console.error("Error al listar administradores:", err));
    }
  }, [modo]);

  const obtenerAdmin = async () => {
    try {
      const res = await fetch(`http://localhost:8000/administradores/${dni}`);
      if (res.ok) {
        const data = await res.json();
        setAdmin(data);
      } else {
        alert("Administrador no encontrado.");
      }
    } catch (err) {
      console.error("Error al obtener administrador:", err);
    }
  };

  const crearAdmin = async () => {
    try {
      const res = await fetch(`http://localhost:8000/administradores/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(admin),
      });
      if (res.ok) {
        alert("Administrador creado correctamente.");
        setAdmin(null);
        setModo("listar");
      } else {
        alert("Error al crear administrador.");
      }
    } catch (err) {
      console.error("Error al crear administrador:", err);
    }
  };

  const actualizarAdmin = async () => {
    try {
      const res = await fetch(`http://localhost:8000/administradores/${dni}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cargo: admin?.cargo,
          permisos: admin?.permisos,
          estado: admin?.estado,
          foto_perfil: admin?.foto_perfil,
        }),
      });
      if (res.ok) {
        alert("Administrador actualizado.");
      } else {
        alert("Error al actualizar.");
      }
    } catch (err) {
      console.error("Error al actualizar administrador:", err);
    }
  };

  const eliminarAdmin = async () => {
    try {
      const res = await fetch(`http://localhost:8000/administradores/${dni}`, {
        method: "DELETE",
      });
      if (res.ok) {
        alert("Administrador eliminado.");
        setModo("listar");
      } else {
        alert("Error al eliminar.");
      }
    } catch (err) {
      console.error("Error al eliminar administrador:", err);
    }
  };

  const camposCrear = [
    "dni",
    "nombre",
    "apellidos",
    "telefono",
    "fecha_nacimiento",
    "email",
    "contrasena",
    "cargo",
    "permisos",
    "estado",
    "foto_perfil",
  ];

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      <div className="flex flex-wrap justify-center gap-3 mb-6 ">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((modoBtn) => (
          <div className="flex justify-center">
          <button
            key={modoBtn}
            onClick={() => {
              setModo(modoBtn as any);
              setAdmin(null);
              setDni("");
            }}
            className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco ${
              modo === modoBtn ? "bg-blue-500 text-white" : "bg-white text-black"
            }`}
          >
            {modoBtn.toUpperCase()}
          </button>
          </div>
        ))}
      </div>

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
          <button onClick={obtenerAdmin} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
            Obtener
          </button>
          </div>
          {admin && (
  <div className="mt-6 p-4 bg-blanco text-negro rounded-[1rem] shadow-md space-y-2">
    <p><strong>DNI:</strong> {admin.dni}</p>
    <p><strong>Cargo:</strong> {admin.cargo}</p>
    <p><strong>Permisos:</strong> {admin.permisos}</p>
    <p><strong>Estado:</strong> {admin.estado}</p>
    {admin.foto_perfil && (
      <img
        src={admin.foto_perfil}
        alt="Foto de perfil"
        className="w-24 h-24 rounded-full mt-4"
      />
    )}
  </div>
)}

        </>
      )}

      {modo === "crear" && (
        <div className="space-y-2">
          {camposCrear.map((campo) => (
            <input
              key={campo}
              type={campo === "fecha_nacimiento" ? "date" : "text"}
              placeholder={campo}
              className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
              value={(admin as any)?.[campo] || ""}
              onChange={(e) =>
                setAdmin((prev) => ({ ...prev, [campo]: e.target.value }))
              }
            />
          ))}
          <div className="flex justify-center">
          <button onClick={crearAdmin} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
            Crear Administrador
          </button>
          </div>
        </div>
      )}

      {modo === "editar" && (
        <>
        <div className="flex justify-center">
          <button onClick={obtenerAdmin} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
            Cargar Admin
          </button>
          </div>
          {admin && (
            <div className="space-y-2 mt-2">
              {["cargo", "permisos", "estado", "foto_perfil"].map((campo) => (
                <input
                  key={campo}
                  type="text"
                  placeholder={campo}
                  value={(admin as any)[campo]}
                  onChange={(e) =>
                    setAdmin((prev) => prev && { ...prev, [campo]: e.target.value })
                  }
                  className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              ))}
              <div className="flex justify-center">
              <button onClick={actualizarAdmin} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
                Guardar Cambios
              </button>
              </div>
            </div>
          )}
        </>
      )}

      {modo === "eliminar" && (
      <div className="flex justify-center">
        <button onClick={eliminarAdmin} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
          Eliminar Administrador
        </button>
        </div>
        
      )}

      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {admins.map((a) => (
            <div key={a.dni} className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4">
              <strong>{a.dni}</strong> - {a.cargo}
              <div>Permisos: {a.permisos}</div>
              <div>Estado: {a.estado}</div>
              <img src={a.foto_perfil} alt="Perfil" className="h-16 w-16 object-cover mt-1" />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

