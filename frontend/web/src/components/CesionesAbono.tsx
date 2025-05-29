import { useState, useEffect } from "react";

export default function CesionesAbono() {
  const dni = localStorage.getItem("dni") || "";
  const token = localStorage.getItem("token");

  const [modo, setModo] = useState<"crear" | "ver" | "editar" | "eliminar">("ver");
  const [mensaje, setMensaje] = useState<string | null>(null);
  const [idCesion, setIdCesion] = useState<number>(0);
  const [cesiones, setCesiones] = useState<any[]>([]);
  const [bono, setBono] = useState<any>(null); // cambiamos de string a objeto

  const [form, setForm] = useState({
    dni_cedente: dni,
    dni_beneficiario: "",
    id_abono: 0,
    fecha_inicio: "",
    fecha_fin: "",
    fecha_cesion: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name.includes("id") ? Number(value) : value,
    }));
  };

  useEffect(() => {
    if (modo === "ver" && token) {
      const fetchCesiones = async () => {
        try {
          const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/cesiones?skip=0&limit=100`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          if (res.ok) {
            const data = await res.json();
            const filtradas = data.filter((cesion: any) => cesion.dni_cedente === dni);
            setCesiones(filtradas);
            setMensaje(`${filtradas.length} cesión(es) encontrada(s).`);
          } else {
            throw new Error("Error al cargar cesiones.");
          }
        } catch (error: any) {
          setMensaje(`Error: ${error.message}`);
        }
      };

      const fetchBono = async () => {
  try {
    const res = await fetch(
      `https://aplicacion-web-m5oa.onrender.com/socio_abonos?skip=0&limit=100`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    if (!res.ok) throw new Error("Error al obtener abonos");

    const data = await res.json();

    // Filtrar por dni y pagado
    const abonosFiltrados = data
      .filter((abono: any) => abono.dni === dni && abono.pagado)
      .sort((a: any, b: any) => new Date(b.fecha_compra).getTime() - new Date(a.fecha_compra).getTime());

    if (abonosFiltrados.length > 0) {
      setBono(abonosFiltrados[0].id_abono);
      setForm((prev) => ({ ...prev, id_abono: abonosFiltrados[0].id_abono }));
    } else {
      setBono(null);
    }
  } catch (err: any) {
    console.error("Error al obtener bono digital:", err);
    setBono(null);
  }
};


      fetchCesiones();
      fetchBono();
    } else {
      setCesiones([]);
      setMensaje(null);
    }
  }, [modo, dni, token]);

  const handleModoSubmit = async () => {
    if (!token) return;

    const headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };

    let endpoint = `https://aplicacion-web-m5oa.onrender.com/cesiones`;
    let options: RequestInit = {};
    let successMsg = "";

    try {
      if (modo === "crear") {
        options = {
          method: "POST",
          headers,
          body: JSON.stringify(form),
        };
        successMsg = "Cesión creada con éxito.";
      } else if (modo === "editar") {
        endpoint += `/${idCesion}`;
        const { dni_cedente, ...datos } = form;
        options = {
          method: "PUT",
          headers,
          body: JSON.stringify(datos),
        };
        successMsg = "Cesión actualizada con éxito.";
      } else if (modo === "eliminar") {
        endpoint += `/${idCesion}`;
        options = {
          method: "DELETE",
          headers,
        };
        successMsg = "Cesión eliminada con éxito.";
      }

      if (modo === "crear" || modo === "editar" || modo === "eliminar") {
        const res = await fetch(endpoint, options);
        if (res.ok) {
          setMensaje(successMsg);
          if (modo !== "eliminar") setModo("ver");
        } else {
          const err = await res.text();
          throw new Error(err);
        }
      }
    } catch (err: any) {
      setMensaje(`Error: ${err.message}`);
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      <h2 className="text-2xl font-bold text-blanco text-center">Gestión de Cesiones de Abono</h2>

      {/* Selector de Modo */}
      <div className="flex justify-center gap-2 flex-wrap">
        {["ver", "crear", "editar", "eliminar"].map((m) => (
          <button
            key={m}
            onClick={() => setModo(m as any)}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            {m[0].toUpperCase() + m.slice(1)}
          </button>
        ))}
      </div>

      {/* ID para editar/eliminar */}
{(modo === "editar" || modo === "eliminar") && (
  <div className="flex flex-col w-[95%]">
    <label htmlFor="id_cesion" className="mb-1 text-sm font-semibold text-white">
      ID CESIÓN
    </label>
    <input
      id="id_cesion"
      type="number"
      placeholder="ID Cesión"
      className="rounded-[1rem] w-[100%] font-poetsen rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
      value={idCesion}
      onChange={(e) => setIdCesion(Number(e.target.value))}
    />
  </div>
)}


      {/* Formulario */}
      {(modo === "crear" || modo === "editar") && (
  <div className="grid grid-cols-2 gap-4">
    {["dni_cedente", "dni_beneficiario", "id_abono", "fecha_inicio", "fecha_fin", "fecha_cesion"].map((field) => (
      <div key={field} className="flex flex-col">
        <label htmlFor={field} className="mb-1 text-sm font-semibold text-white">
          {field.replace(/_/g, " ").toUpperCase()}
        </label>
        <input
          id={field}
          name={field}
          type={field.includes("fecha") ? "date" : field.includes("id") ? "number" : "text"}
          value={(form as any)[field]}
          onChange={handleChange}
          placeholder={field.replace(/_/g, " ")}
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          disabled={field === "dni_cedente"}
        />
      </div>
    ))}
  </div>
)}


      {/* Lista de cesiones en modo "ver" */}
      {modo === "ver" && (
        <div>
          <h3 className="font-semibold mb-2">Cesiones de {dni}</h3>

          {bono ? (
  <p className="whitespace-pre-wrap">ID_Abono actual: {bono}</p>
) : (
  <p>No se encontró información del abono actual.</p>
)}


          {cesiones.length === 0 ? (
            <p>No hay cesiones activas para este usuario.</p>
          ) : (
          <div className="max-w-[20rem] md:max-w-full overflow-x-auto">
        <table>
              <thead>
                <tr className="bg-celeste text-white">
                  <th className="border border-gray-300 p-2">ID Cesión</th>
                  <th className="border border-gray-300 p-2">DNI Beneficiario</th>
                  <th className="border border-gray-300 p-2">ID Abono</th>
                  <th className="border border-gray-300 p-2">Fecha Inicio</th>
                  <th className="border border-gray-300 p-2">Fecha Fin</th>
                  <th className="border border-gray-300 p-2">Fecha Cesión</th>
                </tr>
              </thead>
              <tbody>
                {cesiones.map((c) => (
                  <tr key={c.id_cesion}>
                    <td className="border border-gray-300 p-2 text-center">{c.id_cesion}</td>
                    <td className="border border-gray-300 p-2 text-center">{c.dni_beneficiario}</td>
                    <td className="border border-gray-300 p-2 text-center">{c.id_abono}</td>
                    <td className="border border-gray-300 p-2 text-center">{c.fecha_inicio}</td>
                    <td className="border border-gray-300 p-2 text-center">{c.fecha_fin}</td>
                    <td className="border border-gray-300 p-2 text-center">{c.fecha_cesion}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          )}
        </div>
      )}

      {/* Botón de acción */}
      {(modo === "crear" || modo === "editar" || modo === "eliminar") && (
        <div className="flex justify-center">
          <button
            onClick={handleModoSubmit}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            {modo === "crear"
              ? "Crear Cesión"
              : modo === "editar"
              ? "Modificar Cesión"
              : "Eliminar Cesión"}
          </button>
        </div>
      )}

      {/* Mensaje */}
      {mensaje && <p className="mt-4 text-center">{mensaje}</p>}
    </div>
  );
}

