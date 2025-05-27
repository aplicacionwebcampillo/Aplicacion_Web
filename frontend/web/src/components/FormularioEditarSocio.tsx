import { useState, useEffect } from "react";

export default function FormularioEditarSocio() {
  const [tipoMembresia, setTipoMembresia] = useState("");
  const [estado, setEstado] = useState("");
  const [fotoPerfil, setFotoPerfil] = useState("");
  const [mensaje, setMensaje] = useState("");

  const dni = localStorage.getItem("dni");
  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!dni || !token) return;

    const fetchSocio = async () => {
      try {
        const res = await fetch(`http://localhost:8000/socios/${dni}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.ok) {
          const data = await res.json();
          setTipoMembresia(data.tipo_membresia || "");
          setEstado(data.estado || "");
          setFotoPerfil(data.foto_perfil || "");
        }
      } catch (err) {
        console.error("Error al cargar datos del socio", err);
      }
    };

    fetchSocio();
  }, [dni, token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!dni || !token) return;

    try {
      const res = await fetch(`http://localhost:8000/socios/${dni}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          tipo_membresia: tipoMembresia,
          estado: estado,
          foto_perfil: fotoPerfil,
        }),
      });

      if (res.ok) {
        setMensaje("Datos actualizados correctamente.");
      } else {
        const errorData = await res.json();
        setMensaje("Error al actualizar: " + JSON.stringify(errorData));
      }
    } catch (err) {
      console.error("Error al enviar datos", err);
      setMensaje("Error de red.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      <h2 className="text-xl font-bold mb-4 text-center">Modificar Datos del Socio</h2>

      <div className="flex justify-center">
        <label className="block font-semibold min-w-[10rem]">Tipo de Membresía</label>
        <input
          type="text"
          value={tipoMembresia}
          onChange={(e) => setTipoMembresia(e.target.value)}
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
      </div>

      <div className="flex justify-center">
        <label className="block font-semibold min-w-[10rem]">Estado</label>
        <input
          type="text"
          value={estado}
          onChange={(e) => setEstado(e.target.value)}
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
      </div>

      <div className="flex justify-center">
        <label className="block font-semibold min-w-[10rem]">URL de Foto de Perfil</label>
        <input
          type="text"
          value={fotoPerfil}
          onChange={(e) => setFotoPerfil(e.target.value)}
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
      </div>
      
      <div className="flex justify-center">
      <button
        type="submit"
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
      >
        Guardar Cambios
      </button>

      {mensaje && (
        <p className="mt-2 text-sm text-center text-emerald-600">{mensaje}</p>
      )}
      </div>
    </form>
  );
}

