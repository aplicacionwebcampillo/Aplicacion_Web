import { useState } from "react";

export default function Predicciones() {
  const dni = localStorage.getItem("dni") || "";
  const token = localStorage.getItem("token");

  const [form, setForm] = useState({
    nombre_competicion: "",
    temporada_competicion: "",
    local: "",
    visitante: "",
    resultado_local: 0,
    resultado_visitante: 0,
    pagado: false,
  });

  const [modo, setModo] = useState<"crear" | "editar" | "eliminar">("crear");
  const [mensaje, setMensaje] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleNumero = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: Number(value),
    }));
  };

  const handleSubmit = async () => {
    if (!token || !dni) return;

    const baseUrl = "http://localhost:8000/predice";
    const endpoint =
      modo === "crear"
        ? baseUrl
        : `${baseUrl}/${dni}/${form.nombre_competicion}/${form.temporada_competicion}/${form.local}/${form.visitante}`;

    const options: RequestInit = {
      method: modo === "crear" ? "POST" : modo === "editar" ? "PUT" : "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      ...(modo !== "eliminar" && {
        body: JSON.stringify({
          ...form,
          dni, // solo requerido en creación
        }),
      }),
    };

    try {
      const res = await fetch(endpoint, options);
      if (res.ok) {
        const msg = modo === "crear"
          ? "Predicción creada con éxito.\nRecuerda que debes pagar la predición \nen efectivo al club."
          : modo === "editar"
          ? "Predicción actualizada con éxito.\nRecuerda que debes pagar la predición \nen efectivo al club."
          : "Predicción eliminada con éxito.";
        setMensaje(msg);
      } else {
        const err = await res.text();
        setMensaje(`Error: ${err}`);
      }
    } catch (error) {
      console.error("Error en predicción:", error);
      setMensaje("Error al procesar la solicitud.");
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      <h2 className="text-2xl font-bold text-blanco text-center">Gestión de Predicciones</h2>

      {/* Selector de Modo */}
      <div className="flex justify-center">
        <button onClick={() => setModo("crear")} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">Crear</button>
        <button onClick={() => setModo("editar")} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">Editar</button>
        <button onClick={() => setModo("eliminar")} className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco">Eliminar</button>
      </div>

      {/* Formulario */}
      <div className="grid grid-cols-2 gap-4">
        <input name="nombre_competicion" value={form.nombre_competicion} onChange={handleChange} placeholder="Competición" className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
        <input name="temporada_competicion" value={form.temporada_competicion} onChange={handleChange} placeholder="Temporada" className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
        <input name="local" value={form.local} onChange={handleChange} placeholder="Equipo Local" className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
        <input name="visitante" value={form.visitante} onChange={handleChange} placeholder="Equipo Visitante" className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />

        {modo !== "eliminar" && (
          <>
            <input name="resultado_local" type="number" value={form.resultado_local} onChange={handleNumero} placeholder="Goles Local" className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
            <input name="resultado_visitante" type="number" value={form.resultado_visitante} onChange={handleNumero} placeholder="Goles Visitante" className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
            
            <label className="hidden col-span-2 flex items-center space-x-2">
              <input name="pagado" type="checkbox" checked={form.pagado} onChange={handleChange} />
              <span>¿Pagado?</span>
            </label>
            
          </>
        )}
      </div>

      <div className="flex justify-center">
      <button
        onClick={handleSubmit}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
      >
        {modo === "crear" ? "Crear" : modo === "editar" ? "Actualizar" : "Eliminar"} Predicción
      </button>

      {mensaje && <p className="mt-4 text-center">{mensaje}</p>}
     </div>
    </div>
  );
}

