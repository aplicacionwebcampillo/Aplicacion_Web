import { useState, useEffect } from "react";
import { useSubirImagen } from "../hooks/useSubirImagen"; // ajusta el path si hace falta

export default function FormularioEditarSocio() {
  const [tipoMembresia, setTipoMembresia] = useState("");
  const [estado, setEstado] = useState("");
  const [fotoPerfil, setFotoPerfil] = useState("");
  const [mensaje, setMensaje] = useState("");

  const dni = localStorage.getItem("dni");
  const token = localStorage.getItem("token");

  // Hook para subir imagen
  const { subirImagen, loading: cargandoImagen, error: errorImagen } = useSubirImagen();

  useEffect(() => {
    if (!dni || !token) return;

    const fetchSocio = async () => {
      try {
        const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/socios/${dni}`, {
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

  const handleImagenChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const url = await subirImagen(file);
      if (url) {
        setFotoPerfil(url);
      } else {
        alert("Error al subir la imagen");
      }
    } catch (error) {
      alert("Error al subir la imagen");
      console.error(error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!dni || !token) return;

    try {
      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/socios/${dni}`, {
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
    <form
      onSubmit={handleSubmit}
      className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4"
    >
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

      <div className="flex flex-col items-center w-[90%] mx-auto">
        <label className="block font-semibold mb-2">Foto de Perfil</label>
        <input
          type="file"
          accept="image/*"
          onChange={handleImagenChange}
          className="rounded-[1rem] font-poetsen w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
        {cargandoImagen && <p className="mt-2 text-sm text-yellow-400">Subiendo imagen...</p>}
        {errorImagen && <p className="mt-2 text-sm text-red-600">Error al subir imagen.</p>}

        {fotoPerfil && (
          <img
            src={fotoPerfil}
            alt="Vista previa"
            className="mt-4 w-24 h-24 object-cover rounded-xl"
          />
        )}
      </div>

      <div className="flex justify-center">
        <button
          type="submit"
          className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        >
          Guardar Cambios
        </button>
      </div>

      {mensaje && <p className="mt-2 text-sm text-center text-emerald-600">{mensaje}</p>}
    </form>
  );
}

