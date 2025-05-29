import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Registro() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    dni: "",
    nombre: "",
    apellidos: "",
    telefono: "",
    fecha_nacimiento: "",
    email: "",
    contrasena: "",
  });

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    try {
      await axios.post("https://aplicacion-web-m5oa.onrender.com/usuarios/", formData);
      setSuccess(true);
      setTimeout(() => navigate("/login"), 1500); // Redirige después de éxito
    } catch (err: any) {
      console.error(err);
      setError("No se pudo registrar. Verifica los datos.");
    }
  };

  return (
    <main className="flex justify-center items-center h-full p-[3rem]">
      <section className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem]">
      <h2 className="text-2xl font-bold mb-4 text-center">Registro de Usuario</h2>
      <div className="flex items-center justify-center bg-gray-100 px-4">
      <form
        onSubmit={handleSubmit}
        className="space-y-6"
      >
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        {success && <p className="text-green-500 text-sm mb-2">¡Registro exitoso!</p>}

        <div className="space-y-3">
          {[
            { label: "DNI", name: "dni" },
            { label: "Nombre", name: "nombre" },
            { label: "Apellidos", name: "apellidos" },
            { label: "Teléfono", name: "telefono" },
            { label: "Fecha de nacimiento", name: "fecha_nacimiento", type: "date" },
            { label: "Email", name: "email", type: "email" },
            { label: "Contraseña", name: "contrasena", type: "password" },
          ].map(({ label, name, type = "text" }) => (
            <div key={name}>
              <label className="block text-sm font-medium mb-1">{label}</label>
              <input
                type={type}
                name={name}
                value={formData[name as keyof typeof formData]}
                onChange={handleChange}
                required
                className="w-[90%] rounded-[1rem] border border-gray-300 rounded px-3 py-2"
              />
            </div>
          ))}
        </div>
	
	<div className="flex items-center justify-center bg-gray-100 px-4">
        <button
          type="submit"
          className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
        >
          Registrarse
        </button>
        </div>

        <div className="mt-6 text-center">
              <p>
                ¿Ya tienes cuenta?{" "}
                <button
                  type="button"
                  onClick={() => navigate("/login")}
                  className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-blanco border-rojo bg-blanco text-rojo border-rojo hover:bg-rojo hover:text-blanco"
                >
                  Iniciar Sesión
                </button>
                         
              </p>
            </div>
      </form>
      </div>
     </section>
    </main>
  );
}

