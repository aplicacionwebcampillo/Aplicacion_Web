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
    <div className="p-4 max-w-lg mx-auto space-y-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-2">Validar Pago</h2>

      {/* Selección del modo */}
      <select
        value={modo}
        onChange={(e) => {
          setModo(e.target.value as any);
          setRespuesta(null);
          setError(null);
        }}
        className="border p-2 rounded w-full"
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
        className="border p-2 rounded w-full"
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
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            placeholder="Temporada Competición"
            value={prediceParams.temporada_competicion}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, temporada_competicion: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            placeholder="Local"
            value={prediceParams.local}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, local: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            placeholder="Visitante"
            value={prediceParams.visitante}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, visitante: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            placeholder="Resultado Local"
            value={prediceParams.resultado_local}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, resultado_local: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            placeholder="Resultado Visitante"
            value={prediceParams.resultado_visitante}
            onChange={(e) =>
              setPrediceParams((p) => ({ ...p, resultado_visitante: e.target.value }))
            }
            className="border p-2 rounded w-full"
          />
        </div>
      )}

      <button
        onClick={validarPago}
        className="bg-blue-600 text-white px-4 py-2 rounded mt-2 w-full"
      >
        Validar Pago
      </button>

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

