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

  // Listar todos los usuarios al cargar
  useEffect(() => {
    if (modo === "listar") {
      fetch("http://localhost:8000/usuarios/usuarios/")
        .then((res) => res.json())
        .then(setUsuarios)
        .catch((err) => console.error("Error al listar usuarios:", err));
    }
  }, [modo]);

  // Obtener un usuario por DNI
  const obtenerUsuario = async () => {
    try {
      const res = await fetch(`http://localhost:8000/usuarios/${dni}`);
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
      const res = await fetch(`http://localhost:8000/usuarios/${dni}`, {
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
      const res = await fetch(`http://localhost:8000/usuarios/${dni}`, {
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
    <div className="p-4 space-y-4">
      <div className="flex space-x-2">
        <button onClick={() => setModo("listar")}>Listar Usuarios</button>
        <button onClick={() => setModo("buscar")}>Buscar Usuario</button>
        <button onClick={() => setModo("editar")}>Editar Usuario</button>
        <button onClick={() => setModo("eliminar")}>Eliminar Usuario</button>
      </div>

      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="DNI del usuario"
          value={dni}
          onChange={(e) => setDni(e.target.value)}
          className="border p-2 rounded w-full"
        />
      )}

      {modo === "buscar" && (
        <button onClick={obtenerUsuario} className="bg-blue-500 text-white px-4 py-2 rounded">
          Obtener Usuario
        </button>
      )}

      {modo === "editar" && (
        <>
          <button onClick={obtenerUsuario} className="bg-yellow-500 text-white px-4 py-2 rounded">
            Cargar Usuario
          </button>
          {usuario && (
            <div className="space-y-2 mt-2">
              {["nombre", "apellidos", "telefono", "fecha_nacimiento", "email", "contrasena"].map((field) => (
                <input
                  key={field}
                  type={field === "fecha_nacimiento" ? "date" : "text"}
                  placeholder={field}
                  value={(usuario as any)[field] || ""}
                  onChange={(e) =>
                    setUsuario((prev) => prev && { ...prev, [field]: e.target.value })
                  }
                  className="border p-2 rounded w-full"
                />
              ))}
              <button onClick={actualizarUsuario} className="bg-green-500 text-white px-4 py-2 rounded">
                Guardar Cambios
              </button>
            </div>
          )}
        </>
      )}

      {modo === "eliminar" && (
        <button onClick={eliminarUsuario} className="bg-red-600 text-white px-4 py-2 rounded">
          Eliminar Usuario
        </button>
      )}

      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {usuarios.map((u) => (
            <div key={u.dni} className="p-2 border rounded shadow-sm">
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

