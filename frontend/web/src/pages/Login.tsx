import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function parseJwt(token: string) {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
}

export default function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);


  // Si ya hay token, redirigir automáticamente
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/"); // o a la página principal que quieras
    }
  }, [navigate]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const params = new URLSearchParams();
      params.append("grant_type", "password");
      params.append("username", username);
      params.append("password", password);
      params.append("scope", "");
      params.append("client_id", "");
      params.append("client_secret", "");

      const response = await fetch("https://aplicacion-web-m5oa.onrender.com/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          Accept: "application/json",
        },
        body: params.toString(),
      });

      if (!response.ok) {
        const errorJson = await response.json();
        throw new Error(
          errorJson.detail ? JSON.stringify(errorJson.detail) : "Error al iniciar sesión"
        );
      }

      const data = await response.json();

      // Guardar solo el token (string) en localStorage
      localStorage.setItem("token", data.access_token);

      // Extraer el DNI desde el payload del token y guardarlo
      const payload = parseJwt(data.access_token);
      if (payload && payload.sub) {
        localStorage.setItem("dni", payload.sub);
      }
      
      window.location.reload();
      //navigate("/");
    } catch (err: any) {
      setError(err.message || "Error desconocido");
    } finally {
      setLoading(false);
    }
  }

  // Función para cerrar sesión: limpiar token y recargar login
  //function handleLogout() {
    //localStorage.removeItem("token");
    //localStorage.removeItem("dni");
    //setUsername("");
    //setPassword("");
    //setError(null);
    //window.location.reload();
    //navigate("/login");
  //}

  return (
    <main className="flex justify-center items-center h-full p-[3rem]">
      <section className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem]">
        <h1 className="text-3xl font-bold text-center mb-6">Iniciar sesión</h1>
        <div className="flex items-center justify-center bg-gray-100 px-4">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="username" className="block mb-1 font-semibold">
                Usuario
              </label>
              <input
                id="username"
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-[90%] rounded-[1rem] border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                autoComplete="username"
                disabled={loading}
              />
            </div>

            <div className="relative">
  <label htmlFor="password" className="block mb-1 font-semibold">
    Contraseña
  </label>
  <input
    id="password"
    type={showPassword ? "text" : "password"}
    required
    value={password}
    onChange={(e) => setPassword(e.target.value)}
    className="w-[78%] rounded-[1rem] border border-gray-300 rounded px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-cyan-500" // pr-10 para espacio al botón
    autoComplete="current-password"
    disabled={loading}
  />
  <button
    type="button"
    onClick={() => setShowPassword(prev => !prev)}
    className="absolute right-3 top-1/2 text-gray-500 text-sm"
    tabIndex={-1}
  >
    {showPassword ? "🔓" : "🔒"}
  </button>
</div>

            <div className="flex items-center justify-center bg-gray-100 px-4">
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
              >
                {loading ? "Iniciando..." : "Iniciar sesión"}
              </button>
            </div>
          </form>
        </div>
        <div className="mt-6 text-center">
          <p>
            ¿No tienes cuenta?{" "}
            <button
              type="button"
              onClick={() => navigate("/registro")}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              Regístrate aquí
            </button>
          </p>
        </div>
      </section>
    </main>
  );
}

