import { useState } from "react";

export default function ValidarPago() {
  const [dni, setDni] = useState("");
  const [modo, setModo] = useState<
    "compra" | "predice" | "socio_abono"
  >("compra");

  // Parámetros extra solo para validar predice
  const [prediceParams, setPrediceParams] = useState({
    nombre_competicion: "",
    temporada_competicion: "",
    local: "",
    visitante: "",
    resultado_local: "",
    resultado_visitante: "",
  });

  const [respuesta, setRespuesta] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const validarPago = async () => {
    setRespuesta(null);
    setError(null);

    if (!dni) {
      setError("Debe ingresar DNI");
      return;
    }

    let url = "";
    let query = "";

    try {
      if (modo === "compra") {
        url = `http://localhost:8000/compras/validar_pago/${encodeURIComponent(
          dni
        )}`;
      } else if (modo === "predice") {
        const params = new URLSearchParams();
        Object.entries(prediceParams).forEach(([key, val]) => {
          if (val) params.append(key, val);
        });
        query = params.toString();
        url = `http://localhost:8000/predice/validar_pago/${encodeURIComponent(
          dni
        )}?${query}`;
      } else if (modo === "socio_abono") {
        url = `http://localhost:8000/socio_abonos/validar_pago/${encodeURIComponent(
          dni
        )}`;
      }

      const res = await fetch(url, { method: "PUT" });
      if (res.ok) {
        const text = await res.text();
        setRespuesta(text);
      } else {
        const data = await res.json();
        setError(
          data.detail?.map((d: any) => d.msg).join(", ") || "Error en validación"
        );
      }
    } catch (e) {
      setError("Error en la conexión");
      console.error(e);
    }
  };

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      <h2 className="text-xl font-bold mb-2">Validar Pago</h2>

      {/* Selección del modo */}
      <select
        value={modo}
        onChange={(e) => {
          setModo(e.target.value as any);
          setRespuesta(null);
          setError(null);
        }}
        className="rounded-[1rem] font-poetsen w-[96%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-blanco"
      >
        <option value="compra">Validar Pago Compra</option>
        <option value="predice">Validar Pago Predice</option>
        <option value="socio_abono">Validar Pago Socio Abono</option>
      </select>

      {/* DNI */}
      <input
        type="text"
        placeholder="DNI"
        value={dni}
        onChange={(e) => setDni(e.target.value)}
        className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
      />

      {/* Parámetros extra solo para predice */}
      {modo === "predice" && (
        <div className="space-y-2">
          <input
            type="text"
            placeholder="Nombre Competición"
            value={prediceParams.nombre_competicion}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, nombre_competicion: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="text"
            placeholder="Temporada Competición"
            value={prediceParams.temporada_competicion}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, temporada_competicion: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="text"
            placeholder="Local"
            value={prediceParams.local}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, local: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="text"
            placeholder="Visitante"
            value={prediceParams.visitante}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, visitante: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="text"
            placeholder="Resultado Local"
            value={prediceParams.resultado_local}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, resultado_local: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
          <input
            type="text"
            placeholder="Resultado Visitante"
            value={prediceParams.resultado_visitante}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, resultado_visitante: e.target.value }))
            }
            className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 "
          />
        </div>
      )}
	
      <div className="flex justify-center"> 
      <button
        onClick={validarPago}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
      >
        Validar Pago
      </button>
      </div> 

      {/* Resultado */}
      {respuesta && (
        <div className="bg-green-100 text-green-700 p-3 rounded mt-2 whitespace-pre-wrap">
          Resultado: {respuesta}
        </div>
      )}
      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded mt-2 whitespace-pre-wrap">
          Error: {error}
        </div>
      )}
    </div>
  );
}

