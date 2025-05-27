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

      // Paso 2: crear compra con el id_pedido recibido
      const compraPayload = {
        dni: usuario.dni,
        id_pedido: idPedido,
        fecha_compra: fechaHoy,
        pagado: false,
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
      setMensaje("Compra realizada con éxito. El pago se realizará en efectivo a la entrega del pedido.");
    } catch (error) {
      alert("Error al realizar la compra, inténtalo de nuevo.");
    }
  };

  return (
    <section className="p-6">
      <h2 className="text-2xl mb-4">Tu carrito</h2>
      {carrito.length === 0 ? (
        <p>No hay productos en el carrito.</p>
      ) : (
        <>
          <ul className="space-y-2">
            {carrito.map((item, i) => (
              <li
                key={`${item.producto.id_producto}-${item.talla}-${i}`}
                className="border-b py-2"
              >
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-semibold">{item.producto.nombre}</p>
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

                <div className="flex items-center gap-2 mt-2">
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
                    className="w-16 border rounded px-2 py-1"
                  />
                  <button
                    onClick={() => quitarDelCarrito(item.producto.id_producto, item.talla)}
                    className="text-red-600"
                  >
                    Quitar
                  </button>
                </div>
              </li>
            ))}
          </ul>

          <div className="mt-4 text-lg font-bold">Total: {total} €</div>

          <button
            onClick={crearCompra}
            className="mt-4 bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
          >
            Finalizar compra
          </button>

          {mensaje && (
            <p className="mt-4 text-green-700 font-semibold">{mensaje}</p>
          )}
        </>
      )}
    </section>
  );
}

