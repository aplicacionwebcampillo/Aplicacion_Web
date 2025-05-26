import { createContext, useContext, useState, ReactNode } from "react";

export interface Producto {
  id_producto: number;
  nombre: string;
  descripcion: string;
  precio: number;
  stock: number;
  imagen: string;
}

export interface ProductoEnCarrito {
  producto: Producto;
  talla: string;
  cantidad: number;
}


interface CarritoContextType {
  carrito: Producto[];
  agregarAlCarrito: (producto: Producto) => void;
  quitarDelCarrito: (id_producto: number) => void;
  vaciarCarrito: () => void;
}

const CarritoContext = createContext<CarritoContextType | undefined>(undefined);



export function CarritoProvider({ children }: { children: ReactNode }) {
  const [carrito, setCarrito] = useState<ProductoEnCarrito[]>([]);

  const agregarAlCarrito = (producto: Producto, talla: string) => {
  setCarrito((prev) => {
    const index = prev.findIndex(
      (item) => item.producto.id_producto === producto.id_producto && item.talla === talla
    );

    if (index !== -1) {
      const actualizado = [...prev];
      const item = actualizado[index];
      if (item.cantidad < item.producto.stock) {
        actualizado[index] = { ...item, cantidad: item.cantidad + 1 };
      }
      return actualizado;
    }

    return [...prev, { producto, talla, cantidad: 1 }];
  });
};



  const quitarDelCarrito = (id_producto: number, talla: string) => {
  setCarrito((prev) =>
    prev.filter(
      (item) => !(item.producto.id_producto === id_producto && item.talla === talla)
    )
  );
};



  const vaciarCarrito = () => {
    setCarrito([]);
  };

  return (
    <CarritoContext.Provider
      value={{ carrito, agregarAlCarrito, quitarDelCarrito, vaciarCarrito }}
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

