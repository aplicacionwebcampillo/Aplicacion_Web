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

type Administrador = {
  dni: string;
  cargo: string;
  permisos: string;
  estado: string;
  foto_perfil: string;
};


export default function AdministradorPage() {
  const navigate = useNavigate();
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [adminData, setAdminData] = useState<Administrador | null>(null);
  const [socioData, setSocioData] = useState<null | {
    tipo_membresia: string;
    estado: string;
    foto_perfil: string;
  }>(
    null
  );


  const [formData, setFormData] = useState<Usuario & { contrasena: string }>({
    dni: "",
    nombre: "",
    apellidos: "",
    telefono: "",
    fecha_nacimiento: "",
    email: "",
    contrasena: "",
  });

  const [seccion, setSeccion] = useState<"modificar" | "eliminar" | "admin" | "socio" | "">("modificar");


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
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.ok) {
          const data = await res.json();
          setUsuario(data);
        } else {
          console.error("Error al obtener usuario");
          // Si hay error, forzar logout
          localStorage.removeItem("token");
          localStorage.removeItem("dni");
          navigate("/login");
        }
        
        // Verificar si también es administrador
        try {
          const adminRes = await fetch(`http://localhost:8000/administradores/${dni}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          if (adminRes.ok) {
            const adminInfo = await adminRes.json();
            setAdminData(adminInfo);
          }
        } catch (err) {
          console.log("No es administrador o hubo error al obtener datos de admin.");
        }
      } catch (error) {
        console.error("Error de red al obtener usuario");
        localStorage.removeItem("token");
        localStorage.removeItem("dni");
        navigate("/login");
      }
    };

    fetchUsuario();
  }, [navigate]);
  
  useEffect(() => {
  const token = localStorage.getItem("token");
  const dni = localStorage.getItem("dni");

  if (!token || !dni) return;

  const fetchSocio = async () => {
    try {
      const res = await fetch(`http://localhost:8000/socios/${dni}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        const data = await res.json();
        setSocioData({
          tipo_membresia: data.tipo_membresia,
          estado: data.estado,
          foto_perfil: data.foto_perfil,
        });
      }
    } catch (err) {
      console.error("Error al obtener socio:", err);
    }
  };

  fetchSocio();
}, []);


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

    if (!dni || !token) {
      alert("DNI o token no disponible");
      navigate("/login");
      return;
    }

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
    } catch (err) {
      alert("Error de red");
    }
  };

  const handleEliminar = async () => {
    const confirmar = confirm("¿Estás seguro de eliminar tu cuenta?");
    if (!confirmar) return;

    const dni = localStorage.getItem("dni");
    const token = localStorage.getItem("token");

    if (!dni || !token) {
      alert("DNI o token no disponible");
      navigate("/login");
      return;
    }

    try {
      const res = await fetch(`http://localhost:8000/usuarios/${dni}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
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
    } catch (err) {
      alert("Error de red");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("dni");
    navigate("/login");
  };
  
  const handleAdminChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!adminData) return;
    setAdminData({ ...adminData, [e.target.name]: e.target.value });
  };
  
  const handleSocioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setSocioData({
    ...socioData!,
    [e.target.name]: e.target.value,
  });
};


  const handleActualizarAdmin = async (e: React.FormEvent) => {
    e.preventDefault();
    const dni = localStorage.getItem("dni");
    const token = localStorage.getItem("token");

    if (!dni || !token) {
      alert("DNI o token no disponible");
      navigate("/login");
      return;
    }

    try {
      const res = await fetch(`http://localhost:8000/administradores/${dni}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(adminData),
      });

      if (res.ok) {
        alert("Datos de administrador actualizados correctamente");
        window.location.reload();
      } else {
        const data = await res.json();
        alert("Error al actualizar: " + JSON.stringify(data));
      }
    } catch (err) {
      alert("Error de red");
    }
  };
  
  const handleActualizarSocio = async (e: React.FormEvent) => {
  e.preventDefault();

  const dni = localStorage.getItem("dni");
  const token = localStorage.getItem("token");

  if (!dni || !token || !socioData) return;

  try {
    const res = await fetch(`http://localhost:8000/socios/${dni}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(socioData),
    });

    if (res.ok) {
      alert("Datos de socio actualizados correctamente");
      window.location.reload();
    } else {
      const data = await res.json();
      alert("Error al actualizar socio: " + JSON.stringify(data));
    }
  } catch (err) {
    alert("Error de red");
  }
};


  
  return (
    <div className=" flex flex-col md:flex-row bg-gray-50">
  {/* Menú lateral */}
  <aside className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full m-[1.5rem] max-w-[20rem] max-h-[24rem] md:w-1/4 bg-celeste text-white p-6 space-y-4 flex md:flex-col justify-center md:items-start items-center">
    <button
      onClick={() => setSeccion("modificar")}
      className="w-full max-w-xs px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
    >
      Modificar Usuario
    </button>
    
    {socioData && (
  <button
    onClick={() => setSeccion("socio")}
    className="w-full max-w-xs px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
  >
    Modificar Socio
  </button>
)}
    
    {adminData && (
      <button
        onClick={() => setSeccion("admin")}
        className="w-full max-w-xs px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
      >
        Modificar Administrador
      </button>
    )}

    <button
      onClick={handleLogout}
      className="w-full max-w-xs px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
    >
      Cerrar Sesión
    </button>
    <button
      onClick={() => setSeccion("eliminar")}
      className="w-full max-w-xs px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
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
        <h2 className="text-2xl font-semibold mb-4 text-center text-blanco">Modificar Usuario</h2>
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
              className="w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-[1rem] font-poetsen"
            />
          </div>
        ))}
        <div className="flex justify-center">
          <button
            type="submit"
            className="w-full max-w-[10rem] px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
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
        <button
          onClick={handleEliminar}
          className="w-full px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Confirmar Eliminación
        </button>
      </div>
    )}
    
    {seccion === "admin" && adminData && (
      <form onSubmit={handleActualizarAdmin} className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-md bg-white text-black px-6 py-8 rounded-2xl shadow-lg text-center space-y-4 bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
        <h2 className="text-xl font-semibold text-center">Modificar Datos de Administrador</h2>
    
        <div className="flex flex-col items-center space-y-3">
          <input
            name="cargo"
            value={adminData.cargo}
            onChange={handleAdminChange}
            placeholder="Cargo"
            className="w-[70%] rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-[1rem] font-poetsen"
          />
          <input
            name="permisos"
            value={adminData.permisos}
            onChange={handleAdminChange}
                placeholder="Permisos"
        className="w-[70%] rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-[1rem] font-poetsen"
          />
          <input
            name="estado"
            value={adminData.estado}
            onChange={handleAdminChange}
            placeholder="Estado"
            className="w-[70%] rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-[1rem] font-poetsen"
          />
          <input
            name="foto_perfil"
            value={adminData.foto_perfil}
            onChange={handleAdminChange}
            placeholder="URL Foto de Perfil"
            className="w-[70%] rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-[1rem] font-poetsen"
          />
        </div>

        <div className="flex justify-center">
          <button
            type="submit"
            className="w-full max-w-[10rem] px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
          >
            Guardar Datos de Administrador
          </button>
        </div>
      </form>
    )}
    
    
     {seccion === "socio" && socioData && (
  <form
    onSubmit={handleActualizarSocio}
    className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4"
  >
    <h2 className="text-xl font-semibold text-center">Modificar Datos de Socio</h2>

    <div className="flex flex-col items-center space-y-3">
      <input
        name="tipo_membresia"
        value={socioData.tipo_membresia}
        onChange={handleSocioChange}
        placeholder="Tipo de Membresía"
        className="w-[70%] rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-[1rem] font-poetsen"
      />
      <input
        name="estado"
        value={socioData.estado}
        onChange={handleSocioChange}
        placeholder="Estado"
        className="w-[70%] rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-[1rem] font-poetsen"
      />
      <input
        name="foto_perfil"
        value={socioData.foto_perfil}
        onChange={handleSocioChange}
        placeholder="URL Foto de Perfil"
        className="w-[70%] rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 rounded-[1rem] font-poetsen"
      />
    </div>

    <div className="flex justify-center">
      <button
        type="submit"
        className="w-full max-w-[10rem] px-4 py-2 rounded-full border-2 font-bold transition duration-200 bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
      >
        Guardar Datos de Socio
      </button>
    </div>
  </form>
)}

     
  </main>
</div>

  );
}

