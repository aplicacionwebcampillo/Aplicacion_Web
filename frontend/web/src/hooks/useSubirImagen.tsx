// hooks/useSubirImagen.ts
import { useState } from "react";

export function useSubirImagen() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const subirImagen = async (file: File): Promise<string | null> => {
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", "Aplicacion_Web");

    try {
      const res = await fetch(
        "https://api.cloudinary.com/v1_1/dft3xbtrl/image/upload",
        {
          method: "POST",
          body: formData,
        }
      );
      if (!res.ok) throw new Error("Error al subir imagen");

      const data = await res.json();
      setLoading(false);
      return data.secure_url;
    } catch (err: any) {
      setLoading(false);
      setError(err.message || "Error desconocido");
      return null;
    }
  };

  return { subirImagen, loading, error };
}

