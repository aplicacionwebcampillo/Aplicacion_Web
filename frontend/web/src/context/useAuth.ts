import { useState, useEffect } from "react";

function parseJwt(token: string) {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return null;
  }
}

export function useAuth() {
  const [usuario, setUsuario] = useState<{ dni: string } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setUsuario(null);
      setLoading(false);
      return;
    }
    const payload = parseJwt(token);
    if (payload && payload.sub) {
      setUsuario({ dni: payload.sub });
    } else {
      setUsuario(null);
    }
    setLoading(false);
  }, []);

  const login = (token: string) => {
    localStorage.setItem("token", token);
    const payload = parseJwt(token);
    if (payload && payload.sub) {
      setUsuario({ dni: payload.sub });
    } else {
      setUsuario(null);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUsuario(null);
  };

  return { usuario, loading, login, logout };
}

