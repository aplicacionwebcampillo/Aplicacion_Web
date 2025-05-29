import { useState, useEffect } from "react";
import { useSubirImagen } from "../hooks/useSubirImagen";

interface Patrocinador {
  nombre: string;
  tipo: string;
  email: string;
  telefono: string;
  logo: string;
  fecha_inicio: string;
  fecha_fin: string;
  dni_administrador: string;
}

export default function Patrocinadores() {
  const [modo, setModo] = useState<
    "crear" | "listar" | "buscar" | "editar" | "eliminar"
  >("listar");

  const [nombreBuscado, setNombreBuscado] = useState("");
  const [patrocinador, setPatrocinador] = useState<Patrocinador>({
    nombre: "",
    tipo: "",
    email: "",
    telefono: "",
    logo: "",
    fecha_inicio: "",
    fecha_fin: "",
    dni_administrador: "",
  });

  const [patrocinadores, setPatrocinadores] = useState<Patrocinador[]>([]);
  const { subirImagen, loading: subiendoImagen, error: errorImagen } = useSubirImagen();

  useEffect(() => {
    if (modo === "listar") {
      fetch("https://aplicacion-web-m5oa.onrender.com/patrocinadores/")
        .then((res) => res.json())
        .then(setPatrocinadores)
        .catch((e) => console.error("Error listando patrocinadores:", e));
    }
  }, [modo]);

  const obtenerPatrocinador = async () => {
    try {
      const res = await fetch(
        `https://aplicacion-web-m5oa.onrender.com/patrocinadores/${encodeURIComponent(nombreBuscado)}`
      );
      if (res.ok) {
        const data = await res.json();
        setPatrocinador({ ...data, dni_administrador: "" });
      } else {
        alert("Patrocinador no encontrado");
      }
    } catch (error) {
      console.error("Error al obtener patrocinador:", error);
    }
  };

  const crearPatrocinador = async () => {
    try {
      const res = await fetch("https://aplicacion-web-m5oa.onrender.com/patrocinadores/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patrocinador),
      });
      if (res.ok) {
        alert("Patrocinador creado");
        setPatrocinador({
          nombre: "",
          tipo: "",
          email: "",
          telefono: "",
          logo: "",
          fecha_inicio: "",
          fecha_fin: "",
          dni_administrador: "",
        });
        setModo("listar");
      } else {
        alert("Error al crear patrocinador");
      }
    } catch (error) {
      console.error("Error creando patrocinador:", error);
    }
  };

  const actualizarPatrocinador = async () => {
    try {
      const res = await fetch(
        `https://aplicacion-web-m5oa.onrender.com/patrocinadores/${encodeURIComponent(nombreBuscado)}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(patrocinador),
        }
      );
      if (res.ok) {
        alert("Patrocinador actualizado");
      } else {
        alert("Error al actualizar patrocinador");
      }
    } catch (error) {
      console.error("Error actualizando patrocinador:", error);
    }
  };

  const eliminarPatrocinador = async () => {
    try {
      const res = await fetch(
        `https://aplicacion-web-m5oa.onrender.com/patrocinadores/${encodeURIComponent(nombreBuscado)}`,
        {
          method: "DELETE",
        }
      );
      if (res.ok) {
        alert("Patrocinador eliminado");
        setModo("listar");
      } else {
        alert("Error al eliminar patrocinador");
      }
    } catch (error) {
      console.error("Error eliminando patrocinador:", error);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const url = await subirImagen(file);
      if (url) {
        setPatrocinador((prev) => ({ ...prev, logo: url }));
      } else {
        alert("Error subiendo imagen");
      }
    }
  };

  const renderInputs = () =>
    [
      { label: "Nombre", key: "nombre", type: "text" },
      { label: "Tipo", key: "tipo", type: "text" },
      { label: "Email", key: "email", type: "email" },
      { label: "Teléfono", key: "telefono", type: "text" },
      { label: "Fecha Inicio", key: "fecha_inicio", type: "date" },
      { label: "Fecha Fin", key: "fecha_fin", type: "date" },
      { label: "DNI Administrador", key: "dni_administrador", type: "text" },
    ].map(({ label, key, type }) => (
      <input
        key={key}
        type={type}
        placeholder={label}
        value={patrocinador[key as keyof Patrocinador]}
        onChange={(e) =>
          setPatrocinador((prev) => ({ ...prev, [key]: e.target.value }))
        }
        className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
      />
    ));

  const renderFileInput = () => (
    <div className="space-y-2">
      <label className="block font-poetsen">Logo del patrocinador (imagen)</label>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 border-azul bg-azul text-azul bg-blanco text-azul hover:bg-azul hover:text-blanco
          file:mr-4 file:py-2 file:px-4
          file:rounded-full file:border-0
          file:text-sm file:font-semibold
          file:bg-cyan-50 file:text-cyan-700
          hover:file:bg-cyan-100"
      />
      {subiendoImagen && <p>Subiendo imagen...</p>}
      {errorImagen && <p className="text-red-500">Error: {errorImagen}</p>}
      {patrocinador.logo && (
        <img
          src={patrocinador.logo}
          alt="Vista previa"
          className="w-full h-40 object-contain mt-2"
        />
      )}
    </div>
  );

  return (
    <div className="bg-celeste text-blanco px-6 py-10 rounded-[1rem] font-poetsen font-bold w-full max-w-[40rem] shadow-lg space-y-4">
      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["crear", "listar", "buscar", "editar", "eliminar"].map((m) => (
          <div className="flex justify-center" key={m}>
            <button
              className={`px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 border-azul ${
                modo === m ? "bg-azul text-blanco" : "bg-blanco text-azul hover:bg-azul hover:text-blanco"
              }`}
              onClick={() => {
                setModo(m as any);
                setPatrocinador({
                  nombre: "",
                  tipo: "",
                  email: "",
                  telefono: "",
                  logo: "",
                  fecha_inicio: "",
                  fecha_fin: "",
                  dni_administrador: "",
                });
                setNombreBuscado("");
              }}
            >
              {m.toUpperCase()}
            </button>
          </div>
        ))}
      </div>

      {(modo === "buscar" || modo === "editar" || modo === "eliminar") && (
        <input
          type="text"
          placeholder="Nombre del patrocinador"
          value={nombreBuscado}
          onChange={(e) => setNombreBuscado(e.target.value)}
          className="rounded-[1rem] font-poetsen w-[90%] rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
      )}

      {modo === "buscar" && (
        <>
          <div className="flex justify-center">
            <button
              onClick={obtenerPatrocinador}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              Obtener Patrocinador
            </button>
          </div>
          {patrocinador.nombre && (
            <div className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4">
              <h3 className="font-bold text-xl mb-2">{patrocinador.nombre}</h3>
              <img
                src={patrocinador.logo}
                alt={patrocinador.nombre}
                className="w-full h-48 object-contain mb-2"
              />
              <p><b>Tipo:</b> {patrocinador.tipo}</p>
              <p><b>Email:</b> {patrocinador.email}</p>
              <p><b>Teléfono:</b> {patrocinador.telefono}</p>
              <p><b>Fecha Inicio:</b> {patrocinador.fecha_inicio}</p>
              <p><b>Fecha Fin:</b> {patrocinador.fecha_fin}</p>
            </div>
          )}
        </>
      )}

      {modo === "crear" && (
        <div className="space-y-2 max-w-md">
          {renderInputs()}
          {renderFileInput()}
          <div className="flex justify-center">
            <button
              onClick={crearPatrocinador}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              Crear Patrocinador
            </button>
          </div>
        </div>
      )}

      {modo === "editar" && (
        <>
          <div className="flex justify-center">
            <button
              onClick={obtenerPatrocinador}
              className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
            >
              Cargar Patrocinador
            </button>
          </div>
          {patrocinador.nombre && (
            <div className="space-y-2 max-w-md mt-2">
              {renderInputs()}
              {renderFileInput()}
              <div className="flex justify-center">
                <button
                  onClick={actualizarPatrocinador}
                  className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
                >
                  Guardar Cambios
                </button>
              </div>
            </div>
          )}
        </>
      )}

      {modo === "eliminar" && (
        <div className="flex justify-center">
          <button
            onClick={eliminarPatrocinador}
            disabled={!nombreBuscado}
            className="px-4 py-2 rounded-full border-2 font-bold transition-colors duration-200 bg-blanco text-azul border-azul hover:bg-azul hover:text-blanco"
          >
            Eliminar Patrocinador
          </button>
        </div>
      )}

      {modo === "listar" && (
        <div className="mt-4 space-y-2">
          {patrocinadores.map((p) => (
            <div
              key={p.nombre}
              className="bg-blanco text-negro px-6 py-10 rounded-[1rem] font-poetsen font-bold shadow-lg space-y-4"
            >
              <h3 className="font-bold text-lg">{p.nombre}</h3>
              <img
                src={p.logo}
                alt={p.nombre}
                className="w-full h-32 object-contain my-2"
              />
              <p><b>Tipo:</b> {p.tipo}</p>
              <p><b>Email:</b> {p.email}</p>
              <p><b>Teléfono:</b> {p.telefono}</p>
              <p><b>Inicio:</b> {p.fecha_inicio}</p>
              <p><b>Fin:</b> {p.fecha_fin}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

