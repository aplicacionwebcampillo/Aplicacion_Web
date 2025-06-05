import { useEffect, useState } from "react";
import { useSubirImagen } from "../hooks/useSubirImagen";

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

type Abono = {
  fecha: string;
  [key: string]: any;
};


export default function Socios() {
  const [modo, setModo] = useState<"crear" | "listar" | "buscar" | "editar" | "eliminar">("listar");
  const [dni, setDni] = useState("");
  const [socio, setSocio] = useState<Socio | null>(null);
  const [socios, setSocios] = useState<Socio[]>([]);
  const [showPassword, setShowPassword] = useState(false);


  useEffect(() => {
    if (modo === "listar") {
      fetch("https://aplicacion-web-m5oa.onrender.com/socios/")
        .then((res) => res.json())
        .then(setSocios)
        .catch((err) => console.error("Error al listar socios:", err));
    }
  }, [modo]);

  const obtenerSocio = async () => {
    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/socios/${dni}`);
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
  
  const { subirImagen } = useSubirImagen();

  const handleImagenChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const url = await subirImagen(file);
    if (url) {
      setSocio((prev) => prev ? { ...prev, foto_perfil: url } : null);
    } else {
      alert("Error al subir la imagen");
    }
  };
  
  const crearSocioAbono = async () => {
    try {
      // 1. Obtener todos los abonos
      const abonoRes = await fetch(`https://aplicacion-web-m5oa.onrender.com/abonos/`);
      if (!abonoRes.ok) throw new Error("Error al obtener abonos");

      const abonos = await abonoRes.json();

      if (!abonos.length) {
        alert("No hay abonos disponibles.");
        return;
      }

      // 2. Buscar el abono con la fecha de inicio más reciente
      const abonoMasReciente = abonos.reduce(
  (a: Abono, b: Abono) => (new Date(a.fecha) > new Date(b.fecha) ? a : b)
);


      // 3. Construir el cuerpo del socio_abono
      const fechaHoy = new Date().toISOString().split("T")[0];

      const datosSocioAbono = {
        dni: socio!.dni,
        id_abono: abonoMasReciente.id_abono,
        fecha_compra: fechaHoy,
        pagado: false,
      };

      // 4. Hacer POST a socio_abonos/
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/socio_abonos/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datosSocioAbono),
      });

      if (res.ok) {
        alert("Socio abono creado correctamente.");
        setSocio(null);
        setModo("listar");
      } else {
        alert("Error al crear socio abono.");
      }
    } catch (err) {
      alert("Ocurrió un error al crear el socio abono.");
    }
  };


  const crearSocio = async () => {
    try {
      if (!socio) {
        alert("No hay datos para crear socio");
        return;
      }
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/socios/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(socio),
      });
      if (res.ok) {
        await crearSocioAbono();
        alert("Socio creado correctamente.");
        setSocio(null);
        setModo("listar");
      } else {
        alert("Error al crear socio.");
      }
    } catch (err) {
      
    }
  };

  const actualizarSocio = async () => {
    try {
      if (!socio) {
        alert("No hay datos para actualizar");
        return;
      }
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/socios/${dni}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tipo_membresia: socio.tipo_membresia,
          estado: socio.estado,
          foto_perfil: socio.foto_perfil,
        }),
      });
      if (res.ok) {
        alert("Socio actualizado.");
        setSocio(null);
        setModo("listar");
      } else {
        alert("Error al actualizar socio.");
      }
    } catch (err) {
      
    }
  };

  const eliminarSocio = async () => {
    try {
      // Obtener abonos del socio
      const resAbonos = await fetch(`https://aplicacion-web-m5oa.onrender.com/socio_abonos/?dni=${dni}`);
      if (!resAbonos.ok) {
        alert("Error al obtener abonos del socio");
        return;
      }
      const abonos = await resAbonos.json();

      // Filtrar abonos únicos por id_abono
      const uniqueAbonos = Array.from(new Set(abonos.map((a: any) => a.id_abono))).map((id) =>
        abonos.find((a: any) => a.id_abono === id)
      );

      // Borrar cada abono uno por uno
      for (const abono of uniqueAbonos) {
        const resDeleteAbono = await fetch(`https://aplicacion-web-m5oa.onrender.com/socio_abonos/${dni}/${abono.id_abono}`, {
          method: "DELETE",
        });
        if (!resDeleteAbono.ok) {
          alert(`Error al eliminar el abono ID ${abono.id_abono}`);
          return; // Para no seguir si hay error
        }
      }

      // Borrar socio
      const resDeleteSocio = await fetch(`https://aplicacion-web-m5oa.onrender.com/socios/${dni}`, {
        method: "DELETE",
      });
      if (resDeleteSocio.ok) {
        alert("Socio eliminado.");
        setModo("listar");
        setSocio(null);
        setDni("");
      } else {
        alert("Error al eliminar socio.");
      }
    } catch (err) {
      console.error("Error al eliminar socio:", err);
      alert("Error en la operación");
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
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      {/* Menú de modos */}
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
          <div className="flex justify-center" key={m}> 
            <button
              onClick={() => {
                setModo(m as any);
                setSocio(null);
                setDni("");
              }}
              className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco ${
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
            <button onClick={obtenerSocio} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">
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
      campo === "num_socio" ? null : (
        <div key={campo} className="relative flex justify-center w-[90%] mx-auto">
          {campo === "contrasena" ? (
            <>
              <input
                type={showPassword ? "text" : "password"}
                placeholder={campo}
                className="rounded-[1rem] font-poetsen w-full border border-gray-300 px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                value={(socio as any)?.[campo] || ""}
                onChange={(e) =>
                  setSocio(prev => ({
                    ...prev!,
                    [campo]: e.target.value || "",
                  }))
                }
              />
              <button
                type="button"
                onClick={() => setShowPassword(prev => !prev)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 text-sm"
              >
                {showPassword ? "🔒" : "🔓"}
              </button>
            </>
          ) : (
            <input
              type={campo === "fecha_nacimiento" ? "date" : "text"}
              placeholder={campo}
              className="rounded-[1rem] font-poetsen w-full border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
              value={(socio as any)?.[campo] || ""}
              onChange={(e) =>
                setSocio(prev => ({
                  ...prev!,
                  [campo]: e.target.value || "",
                }))
              }
            />
          )}
        </div>
      )
    ))}

    <input
      type="file"
      accept="image/*"
      onChange={handleImagenChange}
      className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
    />

    {socio?.foto_perfil && (
      <img src={socio.foto_perfil} alt="Vista previa" className="w-24 h-24 object-cover rounded-xl" />
    )}

    <div className="flex justify-center">
      <button
        onClick={crearSocio}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
      >
        Crear Socio
      </button>
    </div>
  </div>
)}


      {/* Editar socio */}
      {modo === "editar" && (
        <>
          <div className="flex justify-center"> 
            <button
              onClick={obtenerSocio}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              Obtener Socio
            </button>
          </div>
          {socio && (
            <div className="space-y-2 mt-4">
              <input
                type="text"
                placeholder="Tipo Membresía"
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                value={socio.tipo_membresia}
                onChange={(e) =>
                  setSocio((prev) => prev ? { ...prev, tipo_membresia: e.target.value } : null)
                }
              />
              <input
                type="text"
                placeholder="Estado"
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                value={socio.estado}
                onChange={(e) =>
                  setSocio((prev) => prev ? { ...prev, estado: e.target.value } : null)
                }
              />
              <input
                type="file"
                accept="image/*"
                onChange={handleImagenChange}
                className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
              />
              {socio.foto_perfil && (
                <img
                  src={socio.foto_perfil}
                  alt="Vista previa"
                  className="w-24 h-24 object-cover rounded-xl"
                />
              )}
              <div className="flex justify-center"> 
                <button
                  onClick={actualizarSocio}
                  className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
                >
                  Actualizar Socio
                </button>
              </div>
            </div>
          )}
        </>
      )}

      {/* Eliminar socio */}
      {modo === "eliminar" && (
        <>
          <div className="flex justify-center"> 
            <button
              onClick={obtenerSocio}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
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
              <div className="flex justify-center mt-4">
                <button
                  onClick={eliminarSocio}
                  className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
                >
                  Eliminar Socio
                </button>
              </div>
            </div>
          )}
        </>
      )}

      {/* Listar socios */}
      {modo === "listar" && (
        <div className="max-h-[20rem] overflow-y-auto">
          {socios.length === 0 && <p>No hay socios para mostrar.</p>}
          {socios.map((s) => (
            <div
              key={s.dni}
              className="mb-4 p-4 bg-blanco text-negro rounded-[1rem] shadow-md flex items-center gap-4"
            >
              {s.foto_perfil && (
                <img
                  src={s.foto_perfil}
                  alt="Foto perfil"
                  className="w-16 h-16 rounded-full"
                />
              )}
              <div>
                <p><strong>DNI:</strong> {s.dni}</p>
                <p><strong>Nombre:</strong> {s.nombre} {s.apellidos}</p>
                <p><strong>Membresía:</strong> {s.tipo_membresia}</p>
                <p><strong>Estado:</strong> {s.estado}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

