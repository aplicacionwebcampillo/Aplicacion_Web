import React, { useEffect, useState } from "react";
import axios from "axios";

type Membresia = {
  dni: string;
  nombre: string;
  apellido: string;
  email: string;
  telefono: string;
  // añade más campos según tu API
};

type AbonoDigital = string;

type CesionActiva = {
  dni_cedente: string;
  dni_beneficiario: string;
  id_abono: number;
  fecha_inicio: string;
  fecha_fin: string;
  fecha_cesion: string;
  id_cesion: number;
} | null;

type Pedido = {
  id_pedido: number;
  descuento: number;
  precio_total: number;
  productos: {
    id_producto: number;
    nombre: string;
    descripcion: string;
    precio: number;
    stock: number;
    imagen: string;
  }[];
};

type PostForo = {
  id: number;
  autor: string;
  contenido: string;
  fecha: string;
};

type Prediccion = {
  dni: string;
  nombre_competicion: string;
  temporada_competicion: string;
  local: string;
  visitante: string;
  resultado_local: number;
  resultado_visitante: number;
  pagado: boolean;
};

const Socio = () => {
  const [dni, setDni] = useState("12345678X"); // Ejemplo, ideal que venga del contexto o login
  const [menuActivo, setMenuActivo] = useState("membresia");

  // Estados para datos
  const [membresia, setMembresia] = useState<Membresia | null>(null);
  const [abonoDigital, setAbonoDigital] = useState<AbonoDigital>("");
  const [cesionActiva, setCesionActiva] = useState<CesionActiva>(null);
  const [pedidos, setPedidos] = useState<Pedido[]>([]);
  const [postsForo, setPostsForo] = useState<PostForo[]>([]);
  const [predicciones, setPredicciones] = useState<Prediccion[]>([]);

  // Formularios y estados auxiliares
  const [editarMembresia, setEditarMembresia] = useState(false);
  const [formMembresia, setFormMembresia] = useState<Membresia | null>(null);
  const [nuevoPostContenido, setNuevoPostContenido] = useState("");
  const [renovarAbonoIdNuevo, setRenovarAbonoIdNuevo] = useState<number | null>(null);
  const [prediccionNueva, setPrediccionNueva] = useState<Partial<Prediccion>>({ dni });

  // Cargas iniciales para cada sección cuando se activa el menú
  useEffect(() => {
    if (menuActivo === "membresia") {
      cargarMembresia();
    } else if (menuActivo === "abono") {
      cargarAbonoDigital();
    } else if (menuActivo === "cesion") {
      cargarCesionActiva();
    } else if (menuActivo === "compras") {
      cargarPedidos();
    } else if (menuActivo === "foro") {
      cargarPostsForo();
    } else if (menuActivo === "predicciones") {
      cargarPredicciones();
    }
  }, [menuActivo]);

  // Funciones API

  // ------------- Mi Membresía ----------------
  const cargarMembresia = async () => {
    try {
      const res = await axios.get(`/socios/${dni}`);
      setMembresia(res.data);
      setFormMembresia(res.data);
    } catch (error) {
      console.error("Error cargando membresía:", error);
    }
  };

  const guardarMembresia = async () => {
    if (!formMembresia) return;
    try {
      await axios.put(`/socios/${dni}`, formMembresia);
      setMembresia(formMembresia);
      setEditarMembresia(false);
      alert("Datos actualizados correctamente");
    } catch (error) {
      console.error("Error guardando membresía:", error);
      alert("Error al actualizar datos");
    }
  };

  // ------------- Mi Abono ----------------
  const cargarAbonoDigital = async () => {
    try {
      const res = await axios.get(`/socio_abonos/socio/${dni}/abono_digital`);
      setAbonoDigital(res.data);
    } catch (error) {
      console.error("Error cargando abono digital:", error);
    }
  };

  const renovarAbono = async () => {
    if (!renovarAbonoIdNuevo) {
      alert("Debes seleccionar un nuevo ID de abono para renovar");
      return;
    }
    try {
      await axios.post(`/socio_abonos/renovar/${dni}/${renovarAbonoIdNuevo}`);
      alert("Abono renovado correctamente");
      cargarAbonoDigital();
    } catch (error) {
      console.error("Error renovando abono:", error);
      alert("Error al renovar abono");
    }
  };

  // ------------- Cesión de Abono ----------------
  const cargarCesionActiva = async () => {
    try {
      const res = await axios.get(`/cesiones/socio/${dni}/cesion_activa`);
      setCesionActiva(res.data || null);
    } catch (error) {
      console.error("Error cargando cesión activa:", error);
      setCesionActiva(null);
    }
  };

  // ------------- Mis Compras ----------------
  const cargarPedidos = async () => {
    try {
      const res = await axios.get(`/pedidos/`); // Si quieres filtrar por dni, ajusta la ruta o el backend
      setPedidos(res.data);
    } catch (error) {
      console.error("Error cargando pedidos:", error);
    }
  };

  const validarPagoCompra = async (dniCompra: string) => {
    try {
      await axios.put(`/compras/validar_pago/${dniCompra}`);
      alert("Pago validado correctamente");
      cargarPedidos();
    } catch (error) {
      console.error("Error validando pago:", error);
      alert("Error al validar pago");
    }
  };

  // ------------- Foro ----------------
  const cargarPostsForo = async () => {
    try {
      const res = await axios.get(`/posts_foro/`);
      setPostsForo(res.data);
    } catch (error) {
      console.error("Error cargando posts foro:", error);
    }
  };

  const crearPostForo = async () => {
    if (!nuevoPostContenido.trim()) {
      alert("El contenido del post no puede estar vacío");
      return;
    }
    try {
      await axios.post(`/posts_foro/`, {
        autor: dni,
        contenido: nuevoPostContenido,
        fecha: new Date().toISOString(),
      });
      setNuevoPostContenido("");
      cargarPostsForo();
    } catch (error) {
      console.error("Error creando post foro:", error);
      alert("Error al crear post");
    }
  };

  // ------------- Predicciones ----------------
  const cargarPredicciones = async () => {
    try {
      const res = await axios.get(`/predice/${dni}/`);
      setPredicciones(res.data);
    } catch (error) {
      console.error("Error cargando predicciones:", error);
    }
  };

  const validarPagoPrediccion = async (pred: Prediccion) => {
    try {
      await axios.put(
        `/predice/${pred.dni}/${encodeURIComponent(
          pred.nombre_competicion
        )}/${encodeURIComponent(pred.temporada_competicion)}/${encodeURIComponent(
          pred.local
        )}/${encodeURIComponent(pred.visitante)}`,
        {
          resultado_local: pred.resultado_local,
          resultado_visitante: pred.resultado_visitante,
          pagado: true,
        }
      );
      alert("Pago validado en predicción");
      cargarPredicciones();
    } catch (error) {
      console.error("Error validando pago predicción:", error);
      alert("Error al validar pago");
    }
  };

  const crearPrediccion = async () => {
    if (
      !prediccionNueva.nombre_competicion ||
      !prediccionNueva.temporada_competicion ||
      !prediccionNueva.local ||
      !prediccionNueva.visitante
    ) {
      alert("Completa todos los campos de la predicción");
      return;
    }
    try {
      await axios.post(`/predice/`, prediccionNueva);
      alert("Predicción creada");
      setPrediccionNueva({ dni });
      cargarPredicciones();
    } catch (error) {
      console.error("Error creando predicción:", error);
      alert("Error al crear predicción");
    }
  };

  // Render componentes para cada menú
  const renderContenido = () => {
    switch (menuActivo) {
      case "membresia":
        return (
          <div>
            <h2>📄 Mi Membresía</h2>
            {!editarMembresia && membresia && (
              <div>
                <p>DNI: {membresia.dni}</p>
                <p>Nombre: {membresia.nombre}</p>
                <p>Apellido: {membresia.apellido}</p>
                <p>Email: {membresia.email}</p>
                <p>Teléfono: {membresia.telefono}</p>
                <button onClick={() => setEditarMembresia(true)}>Editar datos</button>
              </div>
            )}
            {editarMembresia && formMembresia && (
              <div>
                <label>
                  Nombre:{" "}
                  <input
                    type="text"
                    value={formMembresia.nombre}
                    onChange={(e) =>
                      setFormMembresia({ ...formMembresia, nombre: e.target.value })
                    }
                  />
                </label>
                <label>
                  Apellido:{" "}
                  <input
                    type="text"
                    value={formMembresia.apellido}
                    onChange={(e) =>
                      setFormMembresia({ ...formMembresia, apellido: e.target.value })
                    }
                  />
                </label>
                <label>
                  Email:{" "}
                  <input
                    type="email"
                    value={formMembresia.email}
                    onChange={(e) =>
                      setFormMembresia({ ...formMembresia, email: e.target.value })
                    }
                  />
                </label>
                <label>
                  Teléfono:{" "}
                  <input
                    type="text"
                    value={formMembresia.telefono}
                    onChange={(e) =>
                      setFormMembresia({ ...formMembresia, telefono: e.target.value })
                    }
                  />
                </label>
                <button onClick={guardarMembresia}>Guardar</button>{" "}
                <button onClick={() => setEditarMembresia(false)}>Cancelar</button>
              </div>
            )}
          </div>
        );
      case "abono":
        return (
          <div>
            <h2>🎟️ Mi Abono</h2>
            <div>
              <h3>Abono Digital</h3>
              <pre>{abonoDigital || "No hay abono digital disponible"}</pre>
            </div>
            <div>
              <h3>Renovar Abono</h3>
              <label>
                Nuevo ID de Abono:
                <input
                  type="number"
                  value={renovarAbonoIdNuevo || ""}
                  onChange={(e) => setRenovarAbonoIdNuevo(Number(e.target.value))}
                />
              </label>
              <button onClick={renovarAbono}>Renovar Abono</button>
            </div>
          </div>
        );
      case "cesion":
        return (
          <div>
            <h2>🔄 Cesión de Abono</h2>
            {cesionActiva ? (
              <div>
                <p>DNI Cedente: {cesionActiva.dni_cedente}</p>
                <p>DNI Beneficiario: {cesionActiva.dni_beneficiario}</p>
                <p>ID Abono: {cesionActiva.id_abono}</p>
                <p>Fecha Inicio: {cesionActiva.fecha_inicio}</p>
                <p>Fecha Fin: {cesionActiva.fecha_fin}</p>
                <p>Fecha Cesión: {cesionActiva.fecha_cesion}</p>
              </div>
            ) : (
              <p>No tienes ninguna cesión activa.</p>
            )}
          </div>
        );
      case "compras":
        return (
          <div>
            <h2>🛍️ Mis Compras</h2>
            {pedidos.length === 0 && <p>No hay pedidos para mostrar.</p>}
            {pedidos.map((pedido) => (
              <div key={pedido.id_pedido} style={{ border: "1px solid #ccc", marginBottom: 10 }}>
                <p>Pedido ID: {pedido.id_pedido}</p>
                <p>Descuento: {pedido.descuento}</p>
                <p>Precio Total: {pedido.precio_total}</p>
                <p>Productos:</p>
                <ul>
                  {pedido.productos.map((prod) => (
                    <li key={prod.id_producto}>
                      {prod.nombre} - {prod.precio}€
                    </li>
                  ))}
                </ul>
                <button onClick={() => validarPagoCompra(dni)}>Validar Pago</button>
              </div>
            ))}
          </div>
        );
      case "foro":
        return (
          <div>
            <h2>📢 Foro</h2>
            <div>
              <textarea
                rows={3}
                value={nuevoPostContenido}
                onChange={(e) => setNuevoPostContenido(e.target.value)}
                placeholder="Escribe un nuevo post..."
              />
              <br />
              <button onClick={crearPostForo}>Crear Post</button>
            </div>
            <hr />
            <div>
              {postsForo.length === 0 && <p>No hay posts en el foro.</p>}
              {postsForo.map((post) => (
                <div
                  key={post.id}
                  style={{
                    border: "1px solid #ddd",
                    padding: 8,
                    marginBottom: 8,
                    borderRadius: 4,
                  }}
                >
                  <p>
                    <b>{post.autor}</b> - <i>{new Date(post.fecha).toLocaleString()}</i>
                  </p>
                  <p>{post.contenido}</p>
                </div>
              ))}
            </div>
          </div>
        );
      case "predicciones":
        return (
          <div>
            <h2>🎯 Predicciones</h2>
            <div>
              <h3>Nueva Predicción</h3>
              <label>
                Competición:{" "}
                <input
                  type="text"
                  value={prediccionNueva.nombre_competicion || ""}
                  onChange={(e) =>
                    setPrediccionNueva({ ...prediccionNueva, nombre_competicion: e.target.value })
                  }
                />
              </label>
              <label>
                Temporada:{" "}
                <input
                  type="text"
                  value={prediccionNueva.temporada_competicion || ""}
                  onChange={(e) =>
                    setPrediccionNueva({ ...prediccionNueva, temporada_competicion: e.target.value })
                  }
                />
              </label>
              <label>
                Local:{" "}
                <input
                  type="text"
                  value={prediccionNueva.local || ""}
                  onChange={(e) => setPrediccionNueva({ ...prediccionNueva, local: e.target.value })}
                />
              </label>
              <label>
                Visitante:{" "}
                <input
                  type="text"
                  value={prediccionNueva.visitante || ""}
                  onChange={(e) =>
                    setPrediccionNueva({ ...prediccionNueva, visitante: e.target.value })
                  }
                />
              </label>
              <label>
                Resultado Local:{" "}
                <input
                  type="number"
                  value={prediccionNueva.resultado_local || 0}
                  onChange={(e) =>
                    setPrediccionNueva({
                      ...prediccionNueva,
                      resultado_local: Number(e.target.value),
                    })
                  }
                />
              </label>
              <label>
                Resultado Visitante:{" "}
                <input
                  type="number"
                  value={prediccionNueva.resultado_visitante || 0}
                  onChange={(e) =>
                    setPrediccionNueva({
                      ...prediccionNueva,
                      resultado_visitante: Number(e.target.value),
                    })
                  }
                />
              </label>
              <button onClick={crearPrediccion}>Crear Predicción</button>
            </div>
            <hr />
            <div>
              <h3>Predicciones Existentes</h3>
              {predicciones.length === 0 && <p>No tienes predicciones.</p>}
              {predicciones.map((pred) => (
                <div
                  key={`${pred.nombre_competicion}-${pred.temporada_competicion}-${pred.local}-${pred.visitante}`}
                  style={{ border: "1px solid #ccc", marginBottom: 10, padding: 8 }}
                >
                  <p>
                    <b>{pred.nombre_competicion}</b> - {pred.temporada_competicion}
                  </p>
                  <p>
                    {pred.local} {pred.resultado_local} - {pred.visitante} {pred.resultado_visitante}
                  </p>
                  <p>Pagado: {pred.pagado ? "Sí" : "No"}</p>
                  {!pred.pagado && (
                    <button onClick={() => validarPagoPrediccion(pred)}>Validar Pago</button>
                  )}
                </div>
              ))}
            </div>
          </div>
        );
      default:
        return <p>Selecciona una opción del menú.</p>;
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <main style={{ flex: 1, overflowY: "auto", padding: "1rem" }}>{renderContenido()}</main>
      <nav
        style={{
          width: 240,
          borderLeft: "1px solid #ddd",
          padding: "1rem",
          backgroundColor: "#f9f9f9",
        }}
      >
        <h3>Menú Socio</h3>
        <ul style={{ listStyle: "none", padding: 0 }}>
          <li
            style={{
              padding: "0.5rem",
              cursor: "pointer",
              backgroundColor: menuActivo === "membresia" ? "#ddd" : "transparent",
            }}
            onClick={() => setMenuActivo("membresia")}
          >
            Mi Membresía
          </li>
          <li
            style={{
              padding: "0.5rem",
              cursor: "pointer",
              backgroundColor: menuActivo === "abono" ? "#ddd" : "transparent",
            }}
            onClick={() => setMenuActivo("abono")}
          >
            Mi Abono
          </li>
          <li
            style={{
              padding: "0.5rem",
              cursor: "pointer",
              backgroundColor: menuActivo === "cesion" ? "#ddd" : "transparent",
            }}
            onClick={() => setMenuActivo("cesion")}
          >
            Cesión de Abono
          </li>
          <li
            style={{
              padding: "0.5rem",
              cursor: "pointer",
              backgroundColor: menuActivo === "compras" ? "#ddd" : "transparent",
            }}
            onClick={() => setMenuActivo("compras")}
          >
            Mis Compras
          </li>
          <li
            style={{
              padding: "0.5rem",
              cursor: "pointer",
              backgroundColor: menuActivo === "foro" ? "#ddd" : "transparent",
            }}
            onClick={() => setMenuActivo("foro")}
          >
            Foro
          </li>
          <li
            style={{
              padding: "0.5rem",
              cursor: "pointer",
              backgroundColor: menuActivo === "predicciones" ? "#ddd" : "transparent",
            }}
            onClick={() => setMenuActivo("predicciones")}
          >
            Predicciones
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Socio;

