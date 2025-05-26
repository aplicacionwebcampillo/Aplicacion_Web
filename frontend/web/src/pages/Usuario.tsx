import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

type Usuario = {
  dni: string;
  nombre: string;
  apellidos: string;
  telefono: string;
  fecha_nacimiento: string;
  email: string;
};

export default function UsuarioPage() {
  const navigate = useNavigate();
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [formData, setFormData] = useState<Usuario & { contrasena: string }>({
    dni: "",
    nombre: "",
    apellidos: "",
    telefono: "",
    fecha_nacimiento: "",
    email: "",
    contrasena: "",
  });
  const [seccion, setSeccion] = useState<"modificar" | "eliminar">("modificar");

  useEffect(() => {
    const token = localStorage.getItem("token");
    const dni = localStorage.getItem("dni");

    if (!token || !dni) {
      navigate("/login");
      return;
    }

    const fetchUsuario = async () => {
      try {
        const res = await fetch(`http://localhost:8000/usuarios/${dni}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.ok) {
          const data = await res.json();
          setUsuario(data);
        } else {
          localStorage.removeItem("token");
          localStorage.removeItem("dni");
          navigate("/login");
        }
      } catch {
        localStorage.removeItem("token");
        localStorage.removeItem("dni");
        navigate("/login");
      }
    };

    fetchUsuario();
  }, [navigate]);

  useEffect(() => {
    if (usuario) {
      setFormData({ ...usuario, contrasena: "" });
    }
  }, [usuario]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleActualizar = async (e: React.FormEvent) => {
    e.preventDefault();
    const dni = localStorage.getItem("dni");
    const token = localStorage.getItem("token");

    if (!dni || !token) return;

    const datosActualizados: Partial<typeof formData> = {};
    for (const key in formData) {
      const valor = formData[key as keyof typeof formData];
      if (valor && valor.trim() !== "") {
        datosActualizados[key as keyof typeof formData] = valor;
      }
    }

    try {
      const res = await fetch(`http://localhost:8000/usuarios/${dni}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(datosActualizados),
      });

      if (res.ok) {
        alert("Usuario actualizado correctamente");
        window.location.reload();
      } else {
        const data = await res.json();
        alert("Error al actualizar: " + JSON.stringify(data));
      }
    } catch {
      alert("Error de red");
    }
  };

  const handleEliminar = async () => {
    const confirmar = confirm("¿Estás seguro de eliminar tu cuenta?");
    if (!confirmar) return;

    const dni = localStorage.getItem("dni");
    const token = localStorage.getItem("token");

    if (!dni || !token) return;

    try {
      const res = await fetch(`http://localhost:8000/usuarios/${dni}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.ok) {
        localStorage.removeItem("token");
        localStorage.removeItem("dni");
        alert("Usuario eliminado");
        navigate("/login");
      } else {
        const data = await res.json();
        alert("Error al eliminar: " + JSON.stringify(data));
      }
    } catch {
      alert("Error de red");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("dni");
    navigate("/login");
  };

  return (
    <div className="flex flex-col md:flex-row bg-gray-50">
      {/* Menú lateral */}
      <aside className="bg-celeste text-white px-6 py-8 rounded-[1rem] font-poetsen font-bold md:w-full max-w-full m-[1.5rem] md:max-w-[20rem] md:max-h-[24rem] md:w-1/4 flex flex-col justify-center items-center space-y-4">

        <button
          onClick={() => setSeccion("modificar")}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Modificar Usuario
        </button>

        <button
          onClick={() => navigate("/socio")}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Modificar Socio
        </button>

        <button
          onClick={() => navigate("/administrador")}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Modificar Administrador
        </button>

        <button
          onClick={handleLogout}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Cerrar Sesión
        </button>

        <button
          onClick={() => setSeccion("eliminar")}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Eliminar Usuario
        </button>
      </aside>

      {/* Contenido derecho */}
      <main className="flex-1 p-6 flex justify-center items-start">
        {seccion === "modificar" && (
          <form
            onSubmit={handleActualizar}
            className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4"
          >
            <h2 className="text-2xl font-semibold mb-4 text-center">Modificar Usuario</h2>
            {["nombre", "apellidos", "telefono", "fecha_nacimiento", "email", "contrasena"].map((campo) => (
              <div key={campo} className="flex justify-center">
                <input
                  name={campo}
                  type={campo === "fecha_nacimiento" ? "date" : campo === "email" ? "email" : campo === "contrasena" ? "password" : "text"}
                  value={formData[campo as keyof typeof formData]}
                  onChange={handleChange}
                  placeholder={
                    campo === "contrasena" ? "Nueva Contraseña" : campo.charAt(0).toUpperCase() + campo.slice(1)
                  }
                  className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              </div>
            ))}
            <div className="flex justify-center">
              <button
                type="submit"
                className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
              >
                Guardar Cambios
              </button>
            </div>
          </form>
        )}

        {seccion === "eliminar" && (
          <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
            <h2 className="text-2xl font-semibold text-red-600 text-center">Eliminar Usuario</h2>
            <p className="text-center">Esta acción no se puede deshacer. ¿Deseas continuar?</p>
            <div className="flex justify-center">
            <button
              onClick={handleEliminar}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
            > 
              Confirmar Eliminación
            </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

