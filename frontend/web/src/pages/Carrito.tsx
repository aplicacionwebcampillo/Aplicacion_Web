import { useCarrito } from "../context/CarritoContext";
import { useAuth } from "../context/useAuth";
import { useState } from "react";
import type { ProductoEnCarrito } from '../context/CarritoContext';


export default function Carrito() {
  const { carrito, vaciarCarrito, actualizarCantidad, quitarDelCarrito } = useCarrito();
  const { usuario } = useAuth();
  const [mensaje, setMensaje] = useState("");
  const [codigoDescuento, setCodigoDescuento] = useState("");
  const [descuento, setDescuento] = useState(0);

  carrito.reduce((acc: number, item: ProductoEnCarrito) => acc + item.producto.precio * item.cantidad, 0)
  
  const totalSinDescuento = carrito.reduce((acc: number, item: ProductoEnCarrito) =>
  acc + item.producto.precio * item.cantidad, 0
);


  const totalConDescuento = Number((totalSinDescuento * (1 - descuento)).toFixed(2));

  const aplicarDescuento = async () => {
  try {
    const token = localStorage.getItem("token");

    const response = await fetch("https://aplicacion-web-m5oa.onrender.com/carrito/descuento", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ codigo: codigoDescuento }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Error al aplicar descuento");
    }

    const data = await response.json();
    if (data.descuento) {
      setDescuento(data.descuento);
      setMensaje(data.mensaje || "Descuento aplicado correctamente");
    } else {
      throw new Error("No se recibió un descuento válido");
    }

  } catch (error) {
    setMensaje(error.message || "Código inválido o no autorizado.");
    setDescuento(0);
  }
};

  const crearCompra = async () => {
    if (!usuario) {
      alert("Debes iniciar sesión para poder realizar una compra.");
      return;
    }

    try {
      const token = localStorage.getItem("token");
      const fechaHoy = new Date().toISOString().slice(0, 10);

      const pedidoPayload = {
        descuento: descuento,
        precio_total: totalConDescuento,
        productos_ids: carrito.flatMap(item =>
          Array(item.cantidad).fill(item.producto.id_producto)
        )
      };

      const resPedido = await fetch("https://aplicacion-web-m5oa.onrender.com/pedidos/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(pedidoPayload),
      });

      if (!resPedido.ok) {
        throw new Error("Error al crear el pedido");
      }

      const dataPedido = await resPedido.json();
      const idPedido = dataPedido.id_pedido;

      const compraPayload = {
        dni: usuario.dni,
        id_pedido: idPedido,
        fecha_compra: fechaHoy,
        pagado: false,
        productos: carrito.map(item => ({
          id_producto: item.producto.id_producto,
          cantidad: item.cantidad,
          talla: item.talla
        }))
      };

      const resCompra = await fetch("https://aplicacion-web-m5oa.onrender.com/compras/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(compraPayload),
      });

      if (!resCompra.ok) {
        throw new Error("Error al crear la compra");
      }

      await resCompra.json();

      vaciarCarrito();
      alert("Compra realizada con éxito. El pago se realizará en efectivo a la entrega del pedido.");
    } catch (error) {
      alert("Error al realizar la compra, inténtalo de nuevo.");
    }
  };

  return (
    <main className="flex flex-col gap-8 px-4 py-8 max-w-screen-xl mx-auto m-[0%] p-[2%] font-sans">
      <section className="bg-celeste text-blanco px-4 py-8 rounded-[1rem] font-bold font-poetsen">
        <h2 className="text-2xl mb-4 text-center">Tu carrito</h2>
        {carrito.length === 0 ? (
          <p className="text-center text-negro_texto">No hay productos en el carrito.</p>
        ) : (
          <>
            <ul className="space-y-2 text-negro_texto">
              {carrito.map((item, i) => (
                <li
                  key={`${item.producto.id_producto}-${item.talla}-${i}`}
                  className="border-b py-2"
                >
                  <div className="text-negro_texto flex justify-between items-center">
                    <div>
                      <p className="font-semibold text-negro">{item.producto.nombre}</p>
                      <p className="text-sm">Talla: {item.talla}</p>
                    </div>
                    <div className="text-right">
                      <p>{item.producto.precio} € x {item.cantidad}</p>
                      <p className="font-bold">{item.producto.precio * item.cantidad} €</p>
                    </div>
                  </div>
                  <div className="text-negrotexto flex items-center gap-2 mt-2">
                    <label>Cantidad:</label>
                    <input
                      type="number"
                      min="1"
                      max={item.producto.stock}
                      value={item.cantidad}
                      onChange={(e) => {
                        const nuevaCantidad = Number(e.target.value);
                        if (nuevaCantidad > 0 && nuevaCantidad <= item.producto.stock) {
                          actualizarCantidad(item.producto.id_producto, item.talla, nuevaCantidad);
                        }
                      }}
                      className="rounded-[1rem] font-poetsen rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                    />
                    <button
                      onClick={() => quitarDelCarrito(item.producto.id_producto, item.talla)}
                      className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
                    >
                      Quitar
                    </button>
                  </div>
                </li>
              ))}
            </ul>

            <div className="mt-4 text-negro flex gap-4 items-center">
              <input
                type="text"
                placeholder="Código de descuento"
                value={codigoDescuento}
                onChange={(e) => setCodigoDescuento(e.target.value)}
                className="rounded-[1rem] font-poetsen w-[20%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
              />
              <button
                onClick={aplicarDescuento}
                className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
              >
                Aplicar descuento
              </button>
            </div>

            <div className="mt-4 text-lg font-bold text-negro">
              Total: {totalConDescuento} €
              {descuento > 0 && (
                <span className="text-sm text-green-700 ml-2">
                  ({(descuento * 100).toFixed(0)}% aplicado)
                </span>
              )}
            </div>

            <button
              onClick={crearCompra}
              className="mt-4 px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              Finalizar compra
            </button>

            {mensaje && (
              <p className="mt-4 text-green-700 font-semibold">{mensaje}</p>
            )}
          </>
        )}
      </section>
    </main>
  );
}

