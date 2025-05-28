import { useCarrito } from "../context/CarritoContext";
import { useAuth } from "../context/useAuth";
import { useState } from "react";

export default function Carrito() {
  const { carrito, vaciarCarrito, actualizarCantidad, quitarDelCarrito } = useCarrito();
  const { usuario } = useAuth();
  const [mensaje, setMensaje] = useState("");

  const total = carrito.reduce(
    (acc, item) => acc + item.producto.precio * item.cantidad,
    0
  );

  const crearCompra = async () => {
  if (!usuario) {
    alert("Debes iniciar sesión para poder realizar una compra.");
    return;
  }

  try {
    const token = localStorage.getItem("token");
    const fechaHoy = new Date().toISOString().slice(0, 10);

    // Paso 1: crear pedido
    const pedidoPayload = {
      descuento: 0,
      precio_total: total,
      productos_ids: carrito.flatMap(item =>
        Array(item.cantidad).fill(item.producto.id_producto)
      )
    };

    const resPedido = await fetch("http://localhost:8000/pedidos/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(pedidoPayload),
    });

    if (!resPedido.ok) {
      const errorData = await resPedido.json();
      console.error("Error al crear el pedido:", errorData);
      throw new Error("Error al crear el pedido");
    }

    const dataPedido = await resPedido.json();
    const idPedido = dataPedido.id_pedido;

    // Paso 2: crear compra con los productos incluyendo tallas
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

    const resCompra = await fetch("http://localhost:8000/compras/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(compraPayload),
    });

    if (!resCompra.ok) {
      const errorData = await resCompra.json();
      console.error("Error al crear la compra:", errorData);
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
     <section className="bg-celeste text-blanco px-4 py-8  rounded-[1rem] font-bold font-poetsen">
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
                    <p>
                      {item.producto.precio} € x {item.cantidad}
                    </p>
                    <p className="font-bold">
                      {item.producto.precio * item.cantidad} €
                    </p>
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
                    className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
                  >
                    Quitar
                  </button>
                </div>
              </li>
            ))}
          </ul>

          <div className="mt-4 text-lg font-bold text-negro">Total: {total} €</div>

          <button
            onClick={crearCompra}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
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

