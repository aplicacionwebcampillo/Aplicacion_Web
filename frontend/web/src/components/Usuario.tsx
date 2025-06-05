import { useEffect, useState } from "react";

interface Usuario {
  dni: string;
  nombre: string;
  apellidos: string;
  telefono: string;
  fecha_nacimiento: string;
  email: string;
  contrasena?: string; // Solo para PUT
}

export default function Usuario() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [dni, setDni] = useState("");
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [modo, setModo] = useState<"buscar" | "editar" | "eliminar" | "listar">("listar");
  const [showPassword, setShowPassword] = useState(false);


  // Listar todos los usuarios al cargar
  useEffect(() => {
    if (modo === "listar") {
      fetch("https://aplicacion-web-m5oa.onrender.com/usuarios/usuarios/")
        .then((res) => res.json())
        .then(setUsuarios)
        .catch((err) => console.error("Error al listar usuarios:", err));
    }
  }, [modo]);

  // Obtener un usuario por DNI
  const obtenerUsuario = async () => {
    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/usuarios/${dni}`);
      if (res.ok) {
        const data = await res.json();
        setUsuario(data);
      } else {
        alert("Usuario no encontrado.");
        setUsuario(null);
      }
    } catch (err) {
      console.error("Error al obtener usuario:", err);
    }
  };

  // Actualizar usuario
  const actualizarUsuario = async () => {
    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/usuarios/${dni}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(usuario),
      });
      if (res.ok) {
        const data = await res.json();
        alert("Usuario actualizado correctamente.");
        setUsuario(data);
      } else {
        alert("Error al actualizar usuario.");
      }
    } catch (err) {
      console.error("Error al actualizar usuario:", err);
    }
  };

  // Eliminar usuario
  const eliminarUsuario = async () => {
    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/usuarios/${dni}`, {
        method: "DELETE",
      });
      if (res.ok) {
        alert("Usuario eliminado correctamente.");
        setUsuario(null);
        setModo("listar");
      } else {
        alert("Error al eliminar usuario.");
      }
    } catch (err) {
      console.error("Error al eliminar usuario:", err);
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[20rem] md:max-w-[40rem] shadow-lg space-y-4">
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        <button onClick={() => setModo("listar")} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">Listar Usuarios</button>
        <button onClick={() => setModo("buscar")} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">Buscar Usuario</button>
        <button onClick={() => setModo("editar")} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">Editar Usuario</button>
        <button onClick={() => setModo("eliminar")} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">Eliminar Usuario</button>
      </div>

      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="DNI del usuario"
          value={dni}
          onChange={(e) => setDni(e.target.value)}
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
      )}

      {modo === "buscar" && (
  <div className="space-y-4">
  <div className="flex justify-center">
    <button
      onClick={obtenerUsuario}
      className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
    >
      Obtener Usuario
    </button>
    </div>

    {usuario && (
      <div className="mt-6 p-4 bg-blanco text-negro rounded-[1rem] shadow-md space-y-2">
        <p><strong>DNI:</strong> {usuario.dni}</p>
        <p><strong>Nombre:</strong> {usuario.nombre}</p>
        <p><strong>Apellidos:</strong> {usuario.apellidos}</p>
        <p><strong>Teléfono:</strong> {usuario.telefono}</p>
        <p><strong>Fecha Nac:</strong> {usuario.fecha_nacimiento}</p>
        <p><strong>Correo:</strong> {usuario.email}</p>
      </div>
    )}
  </div>
)}


      {modo === "editar" && (
        <>
          <div className="flex justify-center">
          <button onClick={obtenerUsuario} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
            Cargar Usuario
          </button>
          </div>
          {usuario && (
            <div className="space-y-2 mt-2">
              {["nombre", "apellidos", "telefono", "fecha_nacimiento", "email", "contrasena"].map((field) => (
  <div key={field} className="relative flex justify-center w-[90%]">
    {field === "contrasena" ? (
      <>
        <input
          type={showPassword ? "text" : "password"}
          placeholder="contrasena"
          value={(usuario as any)[field] || ""}
          onChange={(e) =>
            setUsuario((prev) => prev && { ...prev, [field]: e.target.value })
          }
          className="rounded-[1rem] font-poetsen w-full border border-gray-300 px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
        <button
          type="button"
          onClick={() => setShowPassword((prev) => !prev)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 text-sm"
        >
          {showPassword ? "🔒" : "🔓"}
        </button>
      </>
    ) : (
      <input
        type={field === "fecha_nacimiento" ? "date" : field === "email" ? "email" : "text"}
        placeholder={field}
        value={(usuario as any)[field] || ""}
        onChange={(e) =>
          setUsuario((prev) => prev && { ...prev, [field]: e.target.value })
        }
        className="rounded-[1rem] font-poetsen w-full border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
      />
    )}
  </div>
))}

              <div className="flex justify-center">
              <button onClick={actualizarUsuario} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
                Guardar Cambios
              </button>
              </div>
            </div>
          )}
        </>
      )}

      {modo === "eliminar" && (
      <div className="flex justify-center">
        <button onClick={eliminarUsuario} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
          Eliminar Usuario
        </button>
      </div>
      )}

      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {usuarios.map((u) => (
            <div key={u.dni} className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4">
              <strong>{u.nombre} {u.apellidos}</strong> - {u.dni}
              <div>{u.email} | {u.telefono}</div>
              <div>Fecha Nac: {u.fecha_nacimiento}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

