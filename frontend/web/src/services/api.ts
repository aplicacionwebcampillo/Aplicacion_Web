const API_BASE = "http://localhost:5173/";

export async function getNoticias() {
  const res = await fetch(`${API_BASE}/noticias`);
  if (!res.ok) throw new Error("Error al obtener noticias");
  return res.json();
}

