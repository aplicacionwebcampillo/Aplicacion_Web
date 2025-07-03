import { useState, useEffect } from "react";


export default function Compras() {
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
        url = `https://aplicacion-web-m5oa.onrender.com/compras/validar_pago/${encodeURIComponent(
          dni
        )}`;
      } else if (modo === "predice") {
        const params = new URLSearchParams();
        Object.entries(prediceParams).forEach(([key, val]) => {
          if (val) params.append(key, val);
        });
        query = params.toString();
        url = `https://aplicacion-web-m5oa.onrender.com/predice/validar_pago/${encodeURIComponent(
          dni
        )}?${query}`;
      } else if (modo === "socio_abono") {
        url = `https://aplicacion-web-m5oa.onrender.com/socio_abonos/validar_pago/${encodeURIComponent(
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
  
  const [seccion, setSeccion] = useState<"compra" | "abono" | "predice">("compra");
const [filtro, setFiltro] = useState<"todos" | "pendientes" | "finalizados">("todos");
const [datos, setDatos] = useState<any[]>([]);

useEffect(() => {
  const fetchData = async () => {
    try {
      let endpoint = "";
      if (seccion === "compra") {
        endpoint = "compras";
      } else if (seccion === "abono") {
        endpoint = "socio_abonos";
      } else {
        endpoint = "predice";
      }

      const res = await fetch(`https://aplicacion-web-m5oa.onrender.com/${endpoint}`);
      const data = await res.json();

      let filtrados = data;
      if (filtro === "pendientes") {
        filtrados = data.filter((item: any) => !item.pagado);
      } else if (filtro === "finalizados") {
        filtrados = data.filter((item: any) => item.pagado);
      }

      setDatos(filtrados);
    } catch (err) {
      console.error("Error al cargar datos", err);
      setDatos([]);
    }
  };

  fetchData();
}, [seccion, filtro]);

const [busquedaPedidoId, setBusquedaPedidoId] = useState("");
const [pedidoBuscado, setPedidoBuscado] = useState<any | null>(null);
const [errorBusqueda, setErrorBusqueda] = useState<string | null>(null);

const buscarPedido = async () => {
  setPedidoBuscado(null);
  setErrorBusqueda(null);

  if (!busquedaPedidoId) {
    setErrorBusqueda("Ingrese un ID de pedido");
    return;
  }

  try {
    const res = await fetch(
      `https://aplicacion-web-m5oa.onrender.com/pedidos/${encodeURIComponent(
        busquedaPedidoId
      )}`
    );
    if (res.ok) {
      const data = await res.json();
      setPedidoBuscado(data);
    } else {
      setErrorBusqueda("Pedido no encontrado");
    }
  } catch (err) {
    console.error(err);
    setErrorBusqueda("Error al buscar el pedido");
  }
};


  return (
  <div className="md:w-full max-w-full m-[1.5rem] md:max-w-[40rem] md:w-1/4">
     <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen w-full max-w-[20rem] sm:max-w-[40rem] space-y-4 shadow-inner ">
  {/* Sección: Compra_Tienda / Abono / Predice */}
  <div className="flex gap-4 justify-center">
    {["compra", "abono", "predice"].map((tipo) => (
      <button
        key={tipo}
        className={`px-4 py-2 rounded-full border font-bold ${
          seccion === tipo
            ? "bg-azul text-blanco border-azul"
            : "px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        }`}
        onClick={() => setSeccion(tipo as any)}
      >
        {tipo === "compra" ? "Tienda" : tipo === "abono" ? "Abono" : "Predice"}
      </button>
    ))}
  </div>

  {/* Subfiltro: Todos / Pendientes / Finalizados */}
  <div className="flex gap-4 justify-center">
    {["todos", "pendientes", "finalizados"].map((f) => (
      <button
        key={f}
        className={`px-4 py-2 rounded-full border font-bold ${
          filtro === f
            ? "bg-azul text-blanco border-azul"
            : "px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
        }`}
        onClick={() => setFiltro(f as any)}
      >
        {f[0].toUpperCase() + f.slice(1)}
      </button>
    ))}
  </div>

  {/* Tabla */}
  <div className="overflow-auto">
    {/* Solo mostrar si es sección compra */}
{seccion === "compra" && (
  <div className="flex flex-col items-center mt-4 space-y-2">
    <div className="flex gap-2">
      <input
        type="number"
        value={busquedaPedidoId}
        onChange={(e) => setBusquedaPedidoId(e.target.value)}
        placeholder="ID de pedido"
        className="border border-gray-300 px-3 py-2 rounded-full"
      />
      <button
        onClick={buscarPedido}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
      >
        Buscar Pedido
      </button>
    </div>
    {errorBusqueda && (
      <p className="text-red-500 font-medium">{errorBusqueda}</p>
    )}
    {pedidoBuscado && (
      <div className="bg-white p-4 border rounded-lg w-full max-w-[40rem] shadow">
        <h3 className="text-lg font-bold mb-2">
          ID Pedido: {pedidoBuscado.id_pedido}
        </h3>
        <p>Total: {pedidoBuscado.precio_total}€</p>
        <p>Descuento: {pedidoBuscado.descuento}%</p>
        <h4 className="font-semibold mt-2">Productos:</h4>
        <ul className="list-disc list-inside">
          {pedidoBuscado.productos.map((prod: any) => (
            <li key={prod.id_producto}>
              {prod.nombre} - {prod.precio}€
            </li>
          ))}
        </ul>
      </div>
    )}
  </div>
)}

    <table className="min-w-full table-auto border-collapse border border-gray-300 mt-4 text-sm text-center">
      <thead className="bg-celeste text-blanco">
        <tr>
          {seccion === "compra" && (
            <>
              <th className="border px-4 py-2">DNI</th>
              <th className="border px-4 py-2">ID Pedido</th>
              <th className="border px-4 py-2">Fecha</th>
              <th className="border px-4 py-2">Pagado</th>
            </>
            
          )}
          {seccion === "abono" && (
            <>
              <th className="border px-4 py-2">DNI</th>
              <th className="border px-4 py-2">ID Abono</th>
              <th className="border px-4 py-2">Fecha</th>
              <th className="border px-4 py-2">Pagado</th>
            </>
          )}
          {seccion === "predice" && (
            <>
              <th className="border px-4 py-2">DNI</th>
              <th className="border px-4 py-2">Competición</th>
              <th className="border px-4 py-2">Temporada</th>
              <th className="border px-4 py-2">Local</th>
              <th className="border px-4 py-2">Visitante</th>
              <th className="border px-4 py-2">Pagado</th>
            </>
          )}
        </tr>
      </thead>
      <tbody>
        {datos.map((item, i) => (
          <tr key={i} className="hover:bg-gray-100">
            {seccion === "compra" && (
              <>
                <td className="border px-4 py-2">{item.dni}</td>
                <td className="border px-4 py-2">{item.id_pedido}</td>
                <td className="border px-4 py-2">{item.fecha_compra}</td>
                <td className="border px-4 py-2">
                  {item.pagado ? "Sí" : "No"}
                </td>
              </>
            )}
            {seccion === "abono" && (
              <>
                <td className="border px-4 py-2">{item.dni}</td>
                <td className="border px-4 py-2">{item.id_abono}</td>
                <td className="border px-4 py-2">{item.fecha_compra}</td>
                <td className="border px-4 py-2">
                  {item.pagado ? "Sí" : "No"}
                </td>
              </>
            )}
            {seccion === "predice" && (
              <>
                <td className="border px-4 py-2">{item.dni}</td>
                <td className="border px-4 py-2">{item.nombre_competicion}</td>
                <td className="border px-4 py-2">{item.temporada_competicion}</td>
                <td className="border px-4 py-2">{item.local}</td>
                <td className="border px-4 py-2">{item.visitante}</td>
                <td className="border px-4 py-2">
                  {item.pagado ? "Sí" : "No"}
                </td>
              </>
            )}
          </tr>
        ))}
      </tbody>
    </table>
    {datos.length === 0 && (
      <p className="text-center text-gray-500 mt-4">No hay datos disponibles.</p>
    )}
  </div>
</div>

    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[20rem] sm:max-w-[40rem] shadow-lg space-y-4 mt-10">
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
        <option value="compra">Validar Pago Compra Tienda</option>
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
	
      
      <div className="flex justify-center "> 
      <button
        onClick={validarPago}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
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
    </div>
  );
}

