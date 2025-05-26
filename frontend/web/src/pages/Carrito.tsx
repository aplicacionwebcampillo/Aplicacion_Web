import { useCarrito } from "../context/CarritoContext";

export default function Carrito() {
  const { carrito, quitarDelCarrito, vaciarCarrito } = useCarrito();

  const total = carrito.reduce((acc, item) => acc + item.producto.precio * item.cantidad, 0);

  const crearPedido = async () => {
    const productos_ids = carrito.map((p) => p.id_producto);
    const res = await fetch("http://localhost:8000/pedidos/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        descuento: 0,
        precio_total: total,
        productos_ids,
      }),
    });

    const pedido = await res.json();
    console.log("Pedido creado:", pedido);

    vaciarCarrito();
    alert("Pedido realizado correctamente");
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
  <li key={`${item.producto.id_producto}-${item.talla}-${i}`} className="border-b py-2">
    <div className="flex justify-between items-center">
      <div>
        <p className="font-semibold">{item.producto.nombre}</p>
        <p className="text-sm">Talla: {item.talla}</p>
      </div>
      <div className="text-right">
        <p>{item.producto.precio} € x {item.cantidad}</p>
        <p className="font-bold">{item.producto.precio * item.cantidad} €</p>
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
            setCarrito((prev) =>
              prev.map((p) =>
                p.producto.id_producto === item.producto.id_producto && p.talla === item.talla
                  ? { ...p, cantidad: nuevaCantidad }
                  : p
              )
            );
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
            onClick={crearPedido}
            className="mt-4 bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
          >
            Finalizar compra
          </button>
        </>
      )}
    </section>
  );
}

