import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export type TipoAdministrador = {
  dni: string;
  cargo: string;
  permisos: string;
  foto_perfil?: string;
  estado?: 'activo' | 'inactivo';
};

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

  const [adminData, setAdminData] = useState<TipoAdministrador | null>(null);

  const [socioData, setSocioData] = useState<null | {
    tipo_membresia: string;
    estado: string;
    foto_perfil: string;
  }>(null);
  const dni = localStorage.getItem("dni") || "";
  const [showPassword, setShowPassword] = useState(false);
  const [esSocio, setEsSocio] = useState(false);
  const [abonoMasReciente, setAbonoMasReciente] = useState<null | {
    temporada: string;
    precio: number;
    fecha_inicio: string;
    fecha_fin: string;
    descripcion: string;
    id_abono: number;
  }>(null);



  const [seccion, setSeccion] = useState<"modificar" | "eliminar" | "admin" | "socio" | "Registrarse como socio" | "">("modificar");
  
  const handleRegistroSocio = async () => {

  const token = localStorage.getItem("token");
  if (!token) {
    alert("Token no encontrado. Por favor inicia sesión.");
    return;
  }

  try {
    // 1. Registrar al socio
    const resSocio = await fetch("https://aplicacion-web-m5oa.onrender.com/socios/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        dni: formData.dni,
        nombre: formData.nombre,
        apellidos: formData.apellidos,
        telefono: formData.telefono,
        fecha_nacimiento: formData.fecha_nacimiento,
        email: formData.email,
        contrasena: formData.contrasena,
        tipo_socio: "abonado",
        tipo_membresia: "anual",
        estado: "activo",
      }),
    });

    if (!resSocio.ok) {
      const data = await resSocio.json();
      alert("Error al registrar socio: " + JSON.stringify(data));
      return;
    }

    // 2. Obtener abono más reciente
    const resAbonos = await fetch("https://aplicacion-web-m5oa.onrender.com/abonos/");
    const abonos = await resAbonos.json();

    if (!Array.isArray(abonos) || abonos.length === 0) {
      alert("No hay abonos disponibles.");
      return;
    }

    const abonoMasReciente = abonos.reduce((a, b) =>
      new Date(a.fecha_inicio) > new Date(b.fecha_inicio) ? a : b
    );

    // 3. Registrar socio_abono
    const resSocioAbono = await fetch("https://aplicacion-web-m5oa.onrender.com/socio_abonos/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        dni: formData.dni,
        id_abono: abonoMasReciente.id_abono,
        fecha_compra: new Date().toISOString().split("T")[0],
        pagado: false,
      }),
    });

    if (!resSocioAbono.ok) {
      const data = await resSocioAbono.json();
      alert("Error al registrar socio_abono: " + JSON.stringify(data));
      return;
    }

    alert("¡Registro como socio completado con éxito!");
    navigate("/socio");
  } catch (error) {
    console.error("Error al registrar socio:", error);
    alert("Error de red al registrar socio.");
  }
};

 useEffect(() => {
  if (!dni) return;

  fetch(`https://aplicacion-web-m5oa.onrender.com/socios/${dni}`)
    .then(res => {
      if (res.ok) {
        setEsSocio(true);
      } else {
        setEsSocio(false);
      }
    })
    .catch(() => setEsSocio(false));
}, [dni]);

useEffect(() => {
  const fetchAbonos = async () => {
    try {
      const res = await fetch("https://aplicacion-web-m5oa.onrender.com/abonos/");
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          const masReciente = data.reduce((a, b) =>
            new Date(a.fecha_inicio) > new Date(b.fecha_inicio) ? a : b
          );
          setAbonoMasReciente(masReciente);
        }
      } else {
        console.error("Error al obtener abonos");
      }
    } catch (err) {
      console.error("Error de red al obtener abonos:", err);
    }
  };

  fetchAbonos();
}, []);



  useEffect(() => {
    const token = localStorage.getItem("token");
    const dni = localStorage.getItem("dni");

    if (!token || !dni) {
      navigate("/login");
      return;
    }

    const fetchUsuario = async () => {
      try {
        const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/usuarios/${dni}`, {
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
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/usuarios/${dni}`, {
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
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/usuarios/${dni}`, {
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
  
  useEffect(() => {
  const token = localStorage.getItem("token");
  const dni = localStorage.getItem("dni");

  if (!token || !dni) return;

  const fetchSocio = async () => {
    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/socios/${dni}`, {
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
    const token = localStorage.getItem("token");
    const dni = localStorage.getItem("dni");

    if (!token || !dni) return;

    const fetchAdmin = async () => {
      try {
        const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/administradores/${dni}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.ok) {
          const adminInfo = await res.json();
          setAdminData(adminInfo);
        }
      } catch (err) {
        console.error("Error al obtener admin:", err);
      }
    };

    fetchAdmin();
  }, []);

  
  return (
    <div className="flex flex-col md:flex-row bg-gray-50">
      {/* Menú lateral */}
      <aside className="bg-celeste text-azul px-6 py-8 rounded-[1rem] font-poetsen font-bold md:w-full max-w-full m-[1.5rem] md:max-w-[20rem] md:max-h-[24rem] md:w-1/4 flex flex-col justify-center items-center space-y-4">

        <button
          onClick={() => setSeccion("modificar")}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Modificar Usuario
        </button>
        {socioData && (
        <button
          onClick={() => navigate("/socio")}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Zona Socio
        </button>
        )}
        
        {adminData && (
        <button
          onClick={() => navigate("/administrador")}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Zona Administrador
        </button>
        )}
        
        {!esSocio  && (
        <button
          onClick={() => setSeccion("Registrarse como socio")}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Registrarse como socio
        </button>
        )}

        <button
          onClick={handleLogout}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Cerrar Sesión
        </button>

        <button
          onClick={() => setSeccion("eliminar")}
          className="min-w-[14rem] px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
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
            {["nombre", "apellidos", "telefono", "fecha_nacimiento", "email", "contrasena"].map((campo) => {
  const isPassword = campo === "contrasena";
  const isDate = campo === "fecha_nacimiento";
  const isEmail = campo === "email";

  return (
    <div key={campo} className="flex justify-center relative w-[90%]">
      <input
        name={campo}
        type={
          isDate ? "date" :
          isEmail ? "email" :
          isPassword ? (showPassword ? "text" : "password") :
          "text"
        }
        value={formData[campo as keyof typeof formData]}
        onChange={handleChange}
        placeholder={
          isPassword ? "Nueva Contraseña" : campo.charAt(0).toUpperCase() + campo.slice(1)
        }
        className="rounded-[1rem] font-poetsen w-full rounded-xl border border-gray-300 px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-cyan-500"
      />
      {isPassword && (
        <button
          type="button"
          onClick={() => setShowPassword(prev => !prev)}
          className="absolute right-3 top-1/2 -translate-y-1/2 w-full text-lg text-gray-600 hover:text-cyan-700"
          tabIndex={-1}
        >
          {showPassword ? "🔓" : "🔒"}
        </button>
      )}
    </div>
  );
})}

            <div className="flex justify-center">
              <button
                type="submit"
                className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
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
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            > 
              Confirmar Eliminación
            </button>
            </div>
          </div>
        )}
        
        {!esSocio &&  seccion === "Registrarse como socio"  && (
          <div className="text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
          <div className="bg-celeste px-6 py-10 rounded-[1rem]">
            <h2 className="text-2xl font-semibold text-red-600 text-center">Registrarse como socio</h2>
            <p className="text-center text-negro_texto">Para disfrutar de los beneficos de socios se tiene que realizar el pago en efectivo. ¿Deseas continuar?</p>
            <div className="flex justify-center">
            <button
              onClick={handleRegistroSocio}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            > 
              Confirmar Registro
            </button>
            </div>
		</div>
            
            <div className="bg-celeste px-6 py-10 rounded-[1rem]">
  <h3 className="text-xl text-center">Abono Actual</h3>
  {abonoMasReciente ? (
    <div className="bg-white text-negro_texto p-4 rounded-lg shadow space-y-1">
      <p><strong>Temporada:</strong> {abonoMasReciente.temporada}</p>
      <p><strong>Precio:</strong> {abonoMasReciente.precio}€</p>
      <p><strong>Inicio:</strong> {abonoMasReciente.fecha_inicio}</p>
      <p><strong>Fin:</strong> {abonoMasReciente.fecha_fin}</p>
      <p ><strong>Descripción:</strong> </p>
      <div className="text-justify flex justify-center text-negro_texto font-poetsen" dangerouslySetInnerHTML={{ __html: abonoMasReciente.descripcion}} />
    </div>
  ) : (
    <p className="text-center">Cargando abono más reciente...</p>
  )}
</div>



          </div>
        )}
        
      </main>
    </div>
  );
}

