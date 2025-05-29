import type { ReactNode } from "react";
import { createContext, useState, useContext } from "react";


export interface Producto {
  id_producto: number;
  nombre: string;
  descripcion: string;
  precio: number;
  stock: number;
  imagen: string;
}

export type ProductoEnCarrito = {
  producto: Producto;
  cantidad: number;
  talla: string;
};


interface CarritoContextType {
  carrito: ProductoEnCarrito[];
  agregarAlCarrito: (producto: Producto, talla: string) => void;
  quitarDelCarrito: (id_producto: number, talla: string) => void;
  actualizarCantidad: (id_producto: number, talla: string, cantidad: number) => void;
  vaciarCarrito: () => void;
}

const CarritoContext = createContext<CarritoContextType | undefined>(undefined);

export function CarritoProvider({ children }: { children: ReactNode }) {
  const [carrito, setCarrito] = useState<ProductoEnCarrito[]>([]);

  const agregarAlCarrito = async (producto: Producto, talla: string) => {
    const token = localStorage.getItem("token");
    const index = carrito.findIndex(
      (item) => item.producto.id_producto === producto.id_producto && item.talla === talla
    );

    if (index !== -1) {
      actualizarCantidad(producto.id_producto, talla, carrito[index].cantidad + 1);
      return;
    }

    try {
      await fetch("https://aplicacion-web-m5oa.onrender.com/carrito/agregar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ id_producto: producto.id_producto, cantidad: 1 }),
      });
      setCarrito((prev) => [...prev, { producto, talla, cantidad: 1 }]);
    } catch (error) {
      console.error("Error al agregar al carrito:", error);
    }
  };

  const quitarDelCarrito = (id_producto: number, talla: string) => {
    setCarrito((prev) =>
      prev.filter(
        (item) => !(item.producto.id_producto === id_producto && item.talla === talla)
      )
    );
  };

  const actualizarCantidad = async (id_producto: number, talla: string, cantidad: number) => {
    const token = localStorage.getItem("token");
    try {
      await fetch(`https://aplicacion-web-m5oa.onrender.com/carrito/actualizar?id_producto=${id_producto}&cantidad=${cantidad}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setCarrito((prev) =>
        prev.map((item) =>
          item.producto.id_producto === id_producto && item.talla === talla
            ? { ...item, cantidad }
            : item
        )
      );
    } catch (error) {
      console.error("Error al actualizar cantidad:", error);
    }
  };

  const vaciarCarrito = () => {
    setCarrito([]);
  };

  return (
    <CarritoContext.Provider
      value={{ carrito, agregarAlCarrito, quitarDelCarrito, actualizarCantidad, vaciarCarrito }}
    >
      {children}
    </CarritoContext.Provider>
  );
}

export function useCarrito() {
  const context = useContext(CarritoContext);
  if (!context) {
    throw new Error("useCarrito debe usarse dentro de CarritoProvider");
  }
  return context;
}

