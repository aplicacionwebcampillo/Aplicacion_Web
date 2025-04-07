CREATE OR REPLACE FUNCTION registrar_usuario(
    p_dni VARCHAR(9),
    p_nombre VARCHAR(50),
    p_apellidos VARCHAR(100),
    p_telefono VARCHAR(15),
    p_fecha_nacimiento DATE,
    p_email VARCHAR(100),
    p_contrasena VARCHAR(255)
)
RETURNS VOID AS $$
BEGIN
    -- Insertar en tabla Usuario
    INSERT INTO Usuario (dni, nombre, apellidos, telefono, fecha_nacimiento, email, contraseña)
    VALUES (p_dni, p_nombre, p_apellidos, p_telefono, p_fecha_nacimiento, p_email, p_contrasena);
    
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION registrar_administrador(
    p_dni VARCHAR(9),
    p_nombre VARCHAR(50),
    p_apellidos VARCHAR(100),
    p_telefono VARCHAR(15),
    p_fecha_nacimiento DATE,
    p_email VARCHAR(100),
    p_contrasena VARCHAR(255),
    p_cargo VARCHAR(50),
    p_permisos VARCHAR(50)
)
RETURNS VOID AS $$
BEGIN
    -- Insertar en tabla Usuario
    INSERT INTO Usuario (dni, nombre, apellidos, telefono, fecha_nacimiento, email, contraseña)
    VALUES (p_dni, p_nombre, p_apellidos, p_telefono, p_fecha_nacimiento, p_email, p_contrasena);
    
    -- Insertar en tabla Administrador
    INSERT INTO Administrador (dni, cargo, permisos, estado)
    VALUES (p_dni, p_cargo, p_permisos, 'activo');
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION modificar_usuario(
    p_dni VARCHAR(9),
    p_nombre VARCHAR(50) DEFAULT NULL,
    p_apellidos VARCHAR(100) DEFAULT NULL,
    p_telefono VARCHAR(15) DEFAULT NULL,
    p_email VARCHAR(100) DEFAULT NULL,
    p_contrasena VARCHAR(255) DEFAULT NULL,
    -- Campos específicos de Socio
    p_tipo_membresia VARCHAR(30) DEFAULT NULL,
    p_foto_perfil VARCHAR(255) DEFAULT NULL,
    p_estado VARCHAR(15) DEFAULT NULL
)
RETURNS VOID AS $$
DECLARE
    es_socio BOOLEAN;
BEGIN
    -- Verificar si es socio
    SELECT EXISTS (SELECT 1 FROM Socio WHERE dni = p_dni) INTO es_socio;
    
    -- Actualizar datos básicos en Usuario
    UPDATE Usuario SET
        nombre = COALESCE(p_nombre, nombre),
        apellidos = COALESCE(p_apellidos, apellidos),
        telefono = COALESCE(p_telefono, telefono),
        email = COALESCE(p_email, email),
        contraseña = CASE 
                        WHEN p_contrasena IS NOT NULL THEN crypt(p_contrasena, gen_salt('bf'))
                        ELSE contraseña 
                     END
    WHERE dni = p_dni;
    
    -- Si es socio, actualizar campos específicos
    IF es_socio THEN
        UPDATE Socio SET
            tipo_membresia = COALESCE(p_tipo_membresia, tipo_membresia),
            foto_perfil = COALESCE(p_foto_perfil, foto_perfil),
            estado = COALESCE(p_estado, estado)
        WHERE dni = p_dni;
        
        -- Validar que el estado sea uno de los permitidos
        IF p_estado IS NOT NULL AND p_estado NOT IN ('activo', 'inactivo', 'suspendido') THEN
            RAISE EXCEPTION 'El estado debe ser uno de: activo, inactivo, suspendido';
        END IF;
    END IF;
    
    -- Si se intentó modificar campos de socio pero no es socio
    IF NOT es_socio AND (p_tipo_membresia IS NOT NULL OR p_foto_perfil IS NOT NULL OR p_estado IS NOT NULL) THEN
        RAISE NOTICE 'El usuario con DNI % no es socio, se ignoraron los campos específicos de socio', p_dni;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION modificar_administrador(
    p_dni VARCHAR(9),
    p_nombre VARCHAR(50) DEFAULT NULL,
    p_apellidos VARCHAR(100) DEFAULT NULL,
    p_telefono VARCHAR(15) DEFAULT NULL,
    p_email VARCHAR(100) DEFAULT NULL,
    p_contrasena VARCHAR(255) DEFAULT NULL,
    p_cargo VARCHAR(50) DEFAULT NULL,
    p_permisos VARCHAR(50) DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
    -- Actualizar datos en Usuario
    UPDATE Usuario SET
        nombre = COALESCE(p_nombre, nombre),
        apellidos = COALESCE(p_apellidos, apellidos),
        telefono = COALESCE(p_telefono, telefono),
        email = COALESCE(p_email, email),
        contraseña = CASE 
                        WHEN p_contrasena IS NOT NULL THEN crypt(p_contrasena, gen_salt('bf'))
                        ELSE contraseña 
                     END
    WHERE dni = p_dni;
    
    -- Actualizar datos específicos en Administrador
    UPDATE Administrador SET
        cargo = COALESCE(p_cargo, cargo),
        permisos = COALESCE(p_permisos, permisos)
    WHERE dni = p_dni;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_usuario(
    p_dni VARCHAR(9)
)
RETURNS VOID AS $$
DECLARE
    tiene_abonos_activos BOOLEAN;
BEGIN
    -- Verificar si tiene abonos activos
    SELECT EXISTS (
        SELECT 1 FROM Socio_Abono sa
        JOIN Abono a ON sa.id_abono = a.id_abono
        WHERE sa.dni = p_dni AND a.fecha_fin >= CURRENT_DATE
    ) INTO tiene_abonos_activos;
    
    IF tiene_abonos_activos THEN
        RAISE EXCEPTION 'No se puede eliminar el aficionado porque tiene abonos activos';
    END IF;
    
    -- Eliminar de Socio primero (por la FK)
    DELETE FROM Socio WHERE dni = p_dni;
    
    -- Luego eliminar de Usuario
    DELETE FROM Usuario WHERE dni = p_dni;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_administrador(
    p_dni VARCHAR(9)
)
RETURNS VOID AS $$
DECLARE
    es_ultimo_admin BOOLEAN;
BEGIN
    -- Verificar si es el último administrador
    SELECT COUNT(*) = 1 INTO es_ultimo_admin
    FROM Administrador
    WHERE estado = 'activo';
    
    IF es_ultimo_admin THEN
        RAISE EXCEPTION 'No se puede eliminar el último administrador activo del sistema';
    END IF;
    
    -- Primero desactivar en Administrador
    UPDATE Administrador SET estado = 'inactivo' WHERE dni = p_dni;
    
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE registrar_socio(
    p_dni VARCHAR(9),
    p_nombre VARCHAR(50),
    p_apellidos VARCHAR(100),
    p_telefono VARCHAR(15),
    p_fecha_nacimiento DATE,
    p_email VARCHAR(100),
    p_contrasena VARCHAR(255),
    p_tipo_membresia VARCHAR(30)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_num_socio VARCHAR(20);
BEGIN
    -- Insertar en tabla Usuario primero
    INSERT INTO Usuario(dni, nombre, apellidos, telefono, fecha_nacimiento, email, contraseña)
    VALUES (p_dni, p_nombre, p_apellidos, p_telefono, p_fecha_nacimiento, p_email, p_contrasena);
    
    -- Generar número de socio único (SOC-YYYYMMDD-XXXX)
    v_num_socio := 'SOC-' || TO_CHAR(CURRENT_DATE, 'YYYYMMDD') || '-' || 
                  LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0');
    
    -- Insertar en tabla Socio
    INSERT INTO Socio(dni, num_socio, tipo_membresia)
    VALUES (p_dni, v_num_socio, p_tipo_membresia);
        
    COMMIT;
END;
$$;


CREATE OR REPLACE PROCEDURE comprar_abono(
    p_dni_socio VARCHAR(9),
    p_id_abono INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_abono_activo BOOLEAN;
BEGIN
    -- Verificar si ya tiene abono activo
    SELECT EXISTS (
        SELECT 1 FROM Socio_Abono sa
        JOIN Abono a ON sa.id_abono = a.id_abono
        WHERE sa.dni = p_dni_socio
        AND a.fecha_fin >= CURRENT_DATE
    ) INTO v_abono_activo;
    
    IF v_abono_activo THEN
        RAISE EXCEPTION 'El socio ya tiene un abono activo';
    END IF;
    
    -- Registrar la compra
    INSERT INTO Socio_Abono(dni, id_abono, pagado)
    VALUES (p_dni_socio, p_id_abono, TRUE);
    
    COMMIT;
END;
$$;


CREATE OR REPLACE PROCEDURE renovar_abono(
    p_dni_socio VARCHAR(9),
    p_id_abono_nuevo INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_dias_restantes INTEGER;
    v_id_abono_actual INTEGER;
BEGIN
    -- Obtener abono actual y días restantes
    SELECT 
        a.id_abono,
        (a.fecha_fin - CURRENT_DATE)
    INTO 
        v_id_abono_actual,
        v_dias_restantes
    FROM Socio_Abono sa
    JOIN Abono a ON sa.id_abono = a.id_abono
    WHERE sa.dni = p_dni_socio
    AND a.fecha_fin >= CURRENT_DATE
    LIMIT 1;
    
    -- Verificar renovación anticipada
    IF v_dias_restantes > 30 THEN
        RAISE EXCEPTION 'Solo puedes renovar tu abono en los últimos 30 días antes de su expiración';
    END IF;
    
    -- Registrar nueva compra
    INSERT INTO Socio_Abono(dni, id_abono, pagado)
    VALUES (p_dni_socio, p_id_abono_nuevo, TRUE);
    
    
    COMMIT;
END;
$$;


CREATE OR REPLACE PROCEDURE cancelar_abono(
    p_dni_socio VARCHAR(9)
)
LANGUAGE plpgsql
AS $$
BEGIN
   
    -- Marcar abono como cancelado (no lo eliminamos para mantener historial)
    UPDATE Socio_Abono
    SET pagado = FALSE -- Marcamos como no pagado para indicar cancelación
    WHERE dni = p_dni_socio
    AND id_abono IN (
        SELECT id_abono FROM Abono
        WHERE fecha_fin >= CURRENT_DATE
    );
    
    
    COMMIT;
END;
$$;


CREATE OR REPLACE FUNCTION obtener_historial_abonos(p_dni_socio VARCHAR(9))
RETURNS TABLE (
    temporada VARCHAR(20),
    fecha_compra DATE,
    precio DECIMAL(10,2),
    estado VARCHAR(20),
    fecha_inicio DATE,
    fecha_fin DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.temporada,
        sa.fecha_compra,
        a.precio,
        CASE 
            WHEN a.fecha_fin < CURRENT_DATE THEN 'Expirado'
            WHEN NOT sa.pagado THEN 'Cancelado'
            ELSE 'Activo'
        END AS estado,
        a.fecha_inicio,
        a.fecha_fin
    FROM Socio_Abono sa
    JOIN Abono a ON sa.id_abono = a.id_abono
    WHERE sa.dni = p_dni_socio
    ORDER BY sa.fecha_compra DESC;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE ceder_abono_temporal(
    p_dni_cedente VARCHAR(9),
    p_dni_beneficiario VARCHAR(9),
    p_fecha_inicio DATE,
    p_fecha_fin DATE
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_abono INTEGER;
BEGIN
    -- Verificar que el cedente tiene abono activo
    SELECT sa.id_abono INTO v_id_abono
    FROM Socio_Abono sa
    JOIN Abono a ON sa.id_abono = a.id_abono
    WHERE sa.dni = p_dni_cedente
    AND a.fecha_fin >= CURRENT_DATE
    AND sa.pagado = TRUE
    LIMIT 1;
    
    IF v_id_abono IS NULL THEN
        RAISE EXCEPTION 'No tienes un abono activo para ceder';
    END IF;
    
    -- Verificar que el beneficiario no tenga abono activo
    PERFORM validar_beneficiario_cesion(p_dni_beneficiario);
    
    -- Registrar la cesión
    INSERT INTO Cesion_Abono(
        dni_cedente,
        dni_beneficiario,
        id_abono,
        fecha_inicio,
        fecha_fin
    ) VALUES (
        p_dni_cedente,
        p_dni_beneficiario,
        v_id_abono,
        p_fecha_inicio,
        p_fecha_fin
    );
    
    COMMIT;
END;
$$;


CREATE OR REPLACE FUNCTION validar_beneficiario_cesion(
    p_dni VARCHAR(9)
)
RETURNS VOID AS $$
DECLARE
    v_es_usuario BOOLEAN;
    v_tiene_abono BOOLEAN;
BEGIN
    -- Verificar que es socio
    SELECT EXISTS (SELECT 1 FROM Usuarui WHERE dni = p_dni) INTO v_es_usuario;
    IF NOT v_es_usuarui THEN
        RAISE EXCEPTION 'El beneficiario debe estar registrado como usuario';
    END IF;
    
    -- Verificar que no tiene abono activo
    SELECT EXISTS (
        SELECT 1 FROM Socio_Abono sa
        JOIN Abono a ON sa.id_abono = a.id_abono
        WHERE sa.dni = p_dni
        AND a.fecha_fin >= CURRENT_DATE
        AND sa.pagado = TRUE
    ) INTO v_tiene_abono;
    
    IF v_tiene_abono THEN
        RAISE EXCEPTION 'El beneficiario ya tiene un abono activo';
    END IF;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW Catalogo_Productos AS
SELECT 
    id_producto,
    nombre,
    descripcion,
    precio,
    CASE 
        WHEN stock > 0 THEN 'Disponible'
        ELSE 'Agotado'
    END AS disponibilidad,
    imagen
FROM Producto
WHERE stock >= 0; -- Solo productos con stock válido


CREATE OR REPLACE FUNCTION evitar_stock_negativo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.stock < 0 THEN
        RAISE EXCEPTION 'No se puede tener stock negativo para ningún producto';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_evitar_stock_negativo
BEFORE UPDATE ON Producto
FOR EACH ROW EXECUTE FUNCTION evitar_stock_negativo();


CREATE OR REPLACE FUNCTION verificar_disponibilidad(
    p_id_producto INTEGER,
    p_cantidad INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    v_stock INTEGER;
BEGIN
    SELECT stock INTO v_stock 
    FROM Producto 
    WHERE id_producto = p_id_producto;
    
    RETURN v_stock >= p_cantidad;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION aplicar_descuento_socio(
    p_precio_original DECIMAL(10,2),
    p_dni_usuario VARCHAR(9)
)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    v_descuento DECIMAL(10,2) := 0;
BEGIN
    IF EXISTS (SELECT 1 FROM Socio WHERE dni = p_dni_usuario) THEN
        v_descuento := p_precio_original * 0.10; -- 10% de descuento
    END IF;
    
    RETURN p_precio_original - v_descuento;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE agregar_producto(
    p_nombre VARCHAR(100),
    p_descripcion TEXT,
    p_precio DECIMAL(10,2),
    p_stock INTEGER,
    p_imagen VARCHAR(255),
    p_categoria VARCHAR(50) DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Producto (
        nombre, 
        descripcion, 
        precio, 
        stock, 
        imagen,
        categoria
    ) VALUES (
        p_nombre,
        p_descripcion,
        p_precio,
        p_stock,
        p_imagen,
        p_categoria
    );
END;
$$;


CREATE OR REPLACE PROCEDURE eliminar_producto(
    p_id_producto INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_en_pedidos BOOLEAN;
BEGIN
    -- Verificar si el producto está en pedidos no pagados
    SELECT EXISTS (
        SELECT 1 FROM Item_Carrito ic
        JOIN Carrito c ON ic.id_carrito = c.id_carrito
        WHERE ic.id_producto = p_id_producto
        AND c.activo = TRUE
    ) INTO v_en_pedidos;
    
    IF v_en_pedidos THEN
        RAISE EXCEPTION 'No se puede eliminar un producto con pedidos pendientes';
    END IF;
    
    -- Eliminar producto
    DELETE FROM Producto WHERE id_producto = p_id_producto;
END;
$$;


CREATE OR REPLACE PROCEDURE modificar_producto(
    p_id_producto INTEGER,
    p_nombre VARCHAR(100) DEFAULT NULL,
    p_descripcion TEXT DEFAULT NULL,
    p_precio DECIMAL(10,2) DEFAULT NULL,
    p_stock INTEGER DEFAULT NULL,
    p_imagen VARCHAR(255) DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Producto SET
        nombre = COALESCE(p_nombre, nombre),
        descripcion = COALESCE(p_descripcion, descripcion),
        precio = COALESCE(p_precio, precio),
        stock = COALESCE(p_stock, stock),
        imagen = COALESCE(p_imagen, imagen)
    WHERE id_producto = p_id_producto;
END;
$$;

------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION obtener_calendario_partidos(
    p_nombre_competicion VARCHAR(100),
    p_temporada VARCHAR(20)
)
RETURNS TABLE (
    local VARCHAR(100),
    visitante VARCHAR(100),
    dia DATE,
    hora TIME,
    estadio VARCHAR(100),
    resultado VARCHAR(20)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.local, p.visitante, p.dia, p.hora, p.estadio, p.resultado
    FROM Partido p
    WHERE p.nombre_competicion = p_nombre_competicion
    AND p.temporada_competicion = p_temporada
    ORDER BY p.dia, p.hora;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE actualizar_resultado_partido(
    p_nombre_competicion VARCHAR(100),
    p_temporada VARCHAR(20),
    p_local VARCHAR(100),
    p_visitante VARCHAR(100),
    p_resultado VARCHAR(20)
)
AS $$
BEGIN
    -- Verificar que el partido existe
    IF NOT EXISTS (
        SELECT 1 FROM Partido 
        WHERE nombre_competicion = p_nombre_competicion
        AND temporada_competicion = p_temporada
        AND local = p_local
        AND visitante = p_visitante
    ) THEN
        RAISE EXCEPTION 'El partido especificado no existe';
    END IF;
    
    -- Verificar que el partido ya ha ocurrido (día <= hoy)
    IF (SELECT dia FROM Partido 
        WHERE nombre_competicion = p_nombre_competicion
        AND temporada_competicion = p_temporada
        AND local = p_local
        AND visitante = p_visitante) > CURRENT_DATE THEN
        RAISE EXCEPTION 'No se puede actualizar el resultado de un partido futuro';
    END IF;
    
    -- Actualizar el resultado
    UPDATE Partido
    SET resultado = p_resultado
    WHERE nombre_competicion = p_nombre_competicion
    AND temporada_competicion = p_temporada
    AND local = p_local
    AND visitante = p_visitante;
    
    
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION obtener_detalle_partido(
    p_nombre_competicion VARCHAR(100),
    p_temporada VARCHAR(20),
    p_local VARCHAR(100),
    p_visitante VARCHAR(100)
)
RETURNS TABLE (
    competicion VARCHAR(100),
    temporada VARCHAR(20),
    fecha DATE,
    hora TIME,
    estadio VARCHAR(100),
    resultado VARCHAR(20)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.nombre_competicion,
        p.temporada_competicion,
        p.dia,
        p.hora,
        p.estadio,
        p.resultado
    FROM Partido p
    WHERE p.nombre_competicion = p_nombre_competicion
    AND p.temporada_competicion = p_temporada
    AND p.local = p_local
    AND p.visitante = p_visitante;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE agregar_competicion(
    p_nombre VARCHAR(100),
    p_temporada VARCHAR(20),
    p_fecha_inicio DATE,
    p_fecha_fin DATE DEFAULT NULL,
    p_estado VARCHAR(20) DEFAULT 'pendiente'
)
AS $$
BEGIN
    -- Validar parámetros
    IF p_nombre IS NULL OR p_temporada IS NULL OR p_fecha_inicio IS NULL THEN
        RAISE EXCEPTION 'Nombre, temporada y fecha de inicio son obligatorios';
    END IF;
    
    IF p_fecha_fin IS NOT NULL AND p_fecha_fin < p_fecha_inicio THEN
        RAISE EXCEPTION 'La fecha de fin no puede ser anterior a la fecha de inicio';
    END IF;
    
    -- Insertar nueva competición
    INSERT INTO Competicion (nombre, temporada, estado, fecha_inicio, fecha_fin)
    VALUES (p_nombre, p_temporada, p_estado, p_fecha_inicio, p_fecha_fin);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE eliminar_competicion(
    p_nombre VARCHAR(100),
    p_temporada VARCHAR(20)
)
AS $$
DECLARE
    v_estado VARCHAR(20);
BEGIN
    -- Obtener estado actual de la competición
    SELECT estado INTO v_estado
    FROM Competicion
    WHERE nombre = p_nombre AND temporada = p_temporada;
    
    -- Validar que existe
    IF NOT FOUND THEN
        RAISE EXCEPTION 'La competición especificada no existe';
    END IF;
    
    -- Validar que no ha comenzado
    IF v_estado != 'pendiente' THEN
        RAISE EXCEPTION 'Solo se pueden eliminar competiciones en estado "pendiente"';
    END IF;
    
    -- Validar que no tiene partidos asociados
    IF EXISTS (
        SELECT 1 FROM Partido 
        WHERE nombre_competicion = p_nombre 
        AND temporada_competicion = p_temporada
    ) THEN
        RAISE EXCEPTION 'No se puede eliminar una competición con partidos asociados';
    END IF;
    
    -- Eliminar la competición
    DELETE FROM Competicion
    WHERE nombre = p_nombre AND temporada = p_temporada;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE modificar_competicion(
    p_nombre_original VARCHAR(100),
    p_temporada_original VARCHAR(20),
    p_nuevo_nombre VARCHAR(100) DEFAULT NULL,
    p_nueva_temporada VARCHAR(20) DEFAULT NULL,
    p_nueva_fecha_inicio DATE DEFAULT NULL,
    p_nueva_fecha_fin DATE DEFAULT NULL,
    p_nuevo_estado VARCHAR(20) DEFAULT NULL
)
AS $$
DECLARE
    v_estado_actual VARCHAR(20);
BEGIN
    -- Obtener estado actual
    SELECT estado INTO v_estado_actual
    FROM Competicion
    WHERE nombre = p_nombre_original AND temporada = p_temporada_original;
    
    -- Validar que existe
    IF NOT FOUND THEN
        RAISE EXCEPTION 'La competición especificada no existe';
    END IF;
    
    -- Validar que no ha comenzado si se intenta modificar datos clave
    IF (p_nuevo_nombre IS NOT NULL OR p_nueva_temporada IS NOT NULL) AND v_estado_actual != 'pendiente' THEN
        RAISE EXCEPTION 'No se pueden modificar nombre o temporada de competiciones ya iniciadas';
    END IF;
    
    -- Validar fechas coherentes
    IF p_nueva_fecha_fin IS NOT NULL AND p_nueva_fecha_inicio IS NOT NULL AND p_nueva_fecha_fin < p_nueva_fecha_inicio THEN
        RAISE EXCEPTION 'La fecha de fin no puede ser anterior a la fecha de inicio';
    END IF;
    
    -- Actualizar los campos proporcionados
    UPDATE Competicion
    SET 
        nombre = COALESCE(p_nuevo_nombre, nombre),
        temporada = COALESCE(p_nueva_temporada, temporada),
        fecha_inicio = COALESCE(p_nueva_fecha_inicio, fecha_inicio),
        fecha_fin = COALESCE(p_nueva_fecha_fin, fecha_fin),
        estado = COALESCE(p_nuevo_estado, estado)
    WHERE nombre = p_nombre_original AND temporada = p_temporada_original;
    
    -- Si cambió el nombre o temporada, actualizar partidos asociados
    IF p_nuevo_nombre IS NOT NULL OR p_nueva_temporada IS NOT NULL THEN
        UPDATE Partido
        SET 
            nombre_competicion = COALESCE(p_nuevo_nombre, nombre_competicion),
            temporada_competicion = COALESCE(p_nueva_temporada, temporada_competicion)
        WHERE nombre_competicion = p_nombre_original 
        AND temporada_competicion = p_temporada_original;
    END IF;
END;
$$ LANGUAGE plpgsql;

-----------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION obtener_plantilla_completa(categoria_equipo VARCHAR(50))
RETURNS TABLE (
    id_jugador INTEGER,
    nombre_jugador VARCHAR(100),
    posicion VARCHAR(50),
    edad INTEGER,
    foto VARCHAR(255),
    biografia TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        j.id_jugador,
        j.nombre AS nombre_jugador,
        j.posicion,
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, j.fecha_nacimiento))::INTEGER AS edad,
        j.foto,
        j.biografia
    FROM 
        Jugador j
        JOIN Equipo e ON j.id_equipo = e.id_equipo
    WHERE 
        e.categoria = categoria_equipo
    ORDER BY 
        j.posicion, j.nombre;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION buscar_jugadores(
    nombre_busqueda VARCHAR(100) DEFAULT NULL,
    posicion_busqueda VARCHAR(50) DEFAULT NULL,
    edad_minima INTEGER DEFAULT NULL,
    edad_maxima INTEGER DEFAULT NULL,
    equipo_id INTEGER DEFAULT NULL,
    categoria_equipo VARCHAR(50) DEFAULT NULL
)
RETURNS TABLE (
    id_jugador INTEGER,
    nombre VARCHAR(100),
    posicion VARCHAR(50),
    edad INTEGER,
    equipo VARCHAR(50),
    foto VARCHAR(255)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        j.id_jugador,
        j.nombre,
        j.posicion,
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, j.fecha_nacimiento))::INTEGER AS edad,
        e.categoria AS equipo,
        j.foto
    FROM 
        Jugador j
        LEFT JOIN Equipo e ON j.id_equipo = e.id_equipo
    WHERE 
        (nombre_busqueda IS NULL OR j.nombre ILIKE '%' || nombre_busqueda || '%')
        AND (posicion_busqueda IS NULL OR j.posicion = posicion_busqueda)
        AND (edad_minima IS NULL OR EXTRACT(YEAR FROM AGE(CURRENT_DATE, j.fecha_nacimiento)) >= edad_minima)
        AND (edad_maxima IS NULL OR EXTRACT(YEAR FROM AGE(CURRENT_DATE, j.fecha_nacimiento)) <= edad_maxima)
        AND (equipo_id IS NULL OR j.id_equipo = equipo_id)
        AND (categoria_equipo IS NULL OR e.categoria = categoria_equipo)
    ORDER BY 
        j.nombre;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE agregar_jugador(
    p_id_equipo INTEGER,
    p_nombre VARCHAR(100),
    p_posicion VARCHAR(50),
    p_fecha_nacimiento DATE,
    p_foto VARCHAR(255) DEFAULT NULL,
    p_biografia TEXT DEFAULT NULL
)
AS $$
DECLARE
    nuevo_id INTEGER;
BEGIN
    -- Insertar el nuevo jugador
    INSERT INTO Jugador (id_equipo, nombre, posicion, fecha_nacimiento, foto, biografia)
    VALUES (p_id_equipo, p_nombre, p_posicion, p_fecha_nacimiento, p_foto, p_biografia)
    RETURNING id_jugador INTO nuevo_id;
    
    -- Actualizar el contador de jugadores en el equipo
    UPDATE Equipo 
    SET num_jugadores = num_jugadores + 1
    WHERE id_equipo = p_id_equipo;
    
    RAISE NOTICE 'Jugador añadido con ID: %', nuevo_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE eliminar_jugador(
    p_id_jugador INTEGER
)
AS $$
DECLARE
    v_id_equipo INTEGER;
    v_en_partido BOOLEAN;
BEGIN
    -- Obtener el equipo del jugador
    SELECT id_equipo INTO v_id_equipo FROM Jugador WHERE id_jugador = p_id_jugador;
    
    IF v_id_equipo IS NULL THEN
        RAISE EXCEPTION 'El jugador con ID % no existe', p_id_jugador;
    END IF;
    
    -- Verificar si el jugador está en algún partido
    SELECT EXISTS (
        SELECT 1 FROM Partido
        WHERE local = v_id_equipo OR visitante = v_id_equipo
    ) INTO v_en_partido;
    
    IF v_en_partido THEN
        RAISE EXCEPTION 'No se puede eliminar el jugador porque está asociado a partidos';
    END IF;
    
    -- Eliminar el jugador
    DELETE FROM Jugador WHERE id_jugador = p_id_jugador;
    
    -- Actualizar el contador de jugadores en el equipo
    UPDATE Equipo 
    SET num_jugadores = num_jugadores - 1
    WHERE id_equipo = v_id_equipo;
    
    RAISE NOTICE 'Jugador con ID % eliminado correctamente', p_id_jugador;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE modificar_jugador(
    p_id_jugador INTEGER,
    p_nuevo_id_equipo INTEGER DEFAULT NULL,
    p_nombre VARCHAR(100) DEFAULT NULL,
    p_posicion VARCHAR(50) DEFAULT NULL,
    p_fecha_nacimiento DATE DEFAULT NULL,
    p_foto VARCHAR(255) DEFAULT NULL,
    p_biografia TEXT DEFAULT NULL
)
AS $$
DECLARE
    v_viejo_id_equipo INTEGER;
BEGIN
    -- Obtener el equipo actual del jugador
    SELECT id_equipo INTO v_viejo_id_equipo FROM Jugador WHERE id_jugador = p_id_jugador;
    
    IF v_viejo_id_equipo IS NULL THEN
        RAISE EXCEPTION 'El jugador con ID % no existe', p_id_jugador;
    END IF;
    
    -- Actualizar los datos del jugador
    UPDATE Jugador
    SET 
        id_equipo = COALESCE(p_nuevo_id_equipo, id_equipo),
        nombre = COALESCE(p_nombre, nombre),
        posicion = COALESCE(p_posicion, posicion),
        fecha_nacimiento = COALESCE(p_fecha_nacimiento, fecha_nacimiento),
        foto = COALESCE(p_foto, foto),
        biografia = COALESCE(p_biografia, biografia)
    WHERE id_jugador = p_id_jugador;
    
    -- Si cambió de equipo, actualizar los contadores
    IF p_nuevo_id_equipo IS NOT NULL AND p_nuevo_id_equipo <> v_viejo_id_equipo THEN
        UPDATE Equipo SET num_jugadores = num_jugadores - 1 WHERE id_equipo = v_viejo_id_equipo;
        UPDATE Equipo SET num_jugadores = num_jugadores + 1 WHERE id_equipo = p_nuevo_id_equipo;
    END IF;
    
    RAISE NOTICE 'Jugador con ID % modificado correctamente', p_id_jugador;
END;
$$ LANGUAGE plpgsql;

-----------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION crear_post_foro(
    p_contenido TEXT,
    p_tipo VARCHAR(20),
    p_dni_autor VARCHAR(9)
)
RETURNS INTEGER AS $$
DECLARE
    nuevo_id INTEGER;
BEGIN
    -- Validar tipo de publicación
    IF p_tipo NOT IN ('discusion', 'encuesta', 'votacion') THEN
        RAISE EXCEPTION 'Tipo de publicación no válido';
    END IF;
    
    -- Insertar la nueva publicación
    INSERT INTO Post_Foro (contenido, tipo)
    VALUES (p_contenido, p_tipo)
    RETURNING id_post INTO nuevo_id;
    
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION editar_post_foro(
    p_id_post INTEGER,
    p_nuevo_contenido TEXT,
    p_dni_editor VARCHAR(9))
RETURNS BOOLEAN AS $$
DECLARE
    es_autor BOOLEAN;
    post_reportado BOOLEAN;
BEGIN
    -- Verificar si el editor es el autor original
    SELECT EXISTS (
        SELECT 1 FROM Autoria_Post
        WHERE id_post = p_id_post AND dni_autor = p_dni_editor
    ) INTO es_autor;
    
    -- Verificar si la publicación está reportada
    SELECT reportado FROM Post_Foro WHERE id_post = p_id_post INTO post_reportado;
    
    -- Solo permitir edición si es el autor y no está reportado
    IF NOT es_autor OR post_reportado THEN
        RAISE EXCEPTION 'No tienes permisos para editar esta publicación';
    END IF;
    
    -- Actualizar contenido
    UPDATE Post_Foro
    SET contenido = p_nuevo_contenido
    WHERE id_post = p_id_post;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_post_foro(
    p_id_post INTEGER,
    p_dni_solicitante VARCHAR(9))
RETURNS BOOLEAN AS $$
DECLARE
    es_autor BOOLEAN;
    es_admin BOOLEAN;
BEGIN
    -- Verificar roles
    SELECT EXISTS (
        SELECT 1 FROM Autoria_Post
        WHERE id_post = p_id_post AND dni_autor = p_dni_solicitante
    ) INTO es_autor;
    
    SELECT EXISTS (
        SELECT 1 FROM Administrador
        WHERE dni = p_dni_solicitante
    ) INTO es_admin;
    
    -- Solo permitir eliminación si es autor o administrador
    IF NOT (es_autor OR es_admin) THEN
        RAISE EXCEPTION 'No tienes permisos para eliminar esta publicación';
    END IF;
    
    -- Eliminar publicación
    DELETE FROM Post_Foro WHERE id_post = p_id_post;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION reportar_post(
    p_id_post INTEGER,
    p_dni_reporter VARCHAR(9),
    p_motivo TEXT
)
RETURNS VOID AS $$
BEGIN
    -- Marcar post como reportado
    UPDATE Post_Foro SET moderado = TRUE WHERE id_post = p_id_post;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION moderar_post(
    p_id_post INTEGER,
    p_dni_admin VARCHAR(9),
    p_accion VARCHAR(10))
RETURNS BOOLEAN AS $$
BEGIN
    -- Verificar que es administrador
    IF NOT EXISTS (SELECT 1 FROM Administrador WHERE dni = p_dni_admin) THEN
        RAISE EXCEPTION 'Solo los administradores pueden moderar contenido';
    END IF;
    
    -- Ejecutar acción de moderación
    IF p_accion = 'eliminar' THEN
        DELETE FROM Post_Foro WHERE id_post = p_id_post;
    ELSIF p_accion = 'aprobar' THEN
        UPDATE Post_Foro SET moderado = FALSE WHERE id_post = p_id_post;
    ELSE
        RAISE EXCEPTION 'Acción de moderación no válida';
    END IF;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION crear_encuesta(
    p_contenido TEXT,
    p_opciones TEXT,  -- Opciones como texto separado por comas
    p_dni_autor VARCHAR(9)
)
RETURNS INTEGER AS $$
DECLARE
    post_id INTEGER;
BEGIN
    -- Validar que el autor es socio
    IF NOT EXISTS (SELECT 1 FROM Socio WHERE dni = p_dni_autor) THEN
        RAISE EXCEPTION 'Solo los socios pueden crear encuestas';
    END IF;
    
    -- Crear el post con las opciones en el contenido
    -- Formato: "Pregunta?|opcion1,opcion2,opcion3"
    INSERT INTO Post_Foro (contenido, tipo)
    VALUES (p_contenido || '|' || p_opciones, 'encuesta')
    RETURNING id_post INTO post_id;
    
    RETURN post_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION crear_votacion(
    p_contenido TEXT,
    p_dni_autor VARCHAR(9)
)
RETURNS INTEGER AS $$
DECLARE
    post_id INTEGER;
BEGIN
    -- Validar que el autor es socio
    IF NOT EXISTS (SELECT 1 FROM Socio WHERE dni = p_dni_autor) THEN
        RAISE EXCEPTION 'Solo los socios pueden crear votaciones';
    END IF;
    
    -- Crear el post de votación
    INSERT INTO Post_Foro (contenido, tipo)
    VALUES (p_contenido, 'votacion')
    RETURNING id_post INTO post_id;
    
    RETURN post_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION registrar_voto(
    p_id_post INTEGER,
    p_dni_votante VARCHAR(9),
    p_opcion INTEGER DEFAULT NULL)  -- Para encuestas
RETURNS BOOLEAN AS $$
DECLARE
    post_record RECORD;
    es_socio BOOLEAN;
    opciones TEXT[];
    voto_previo BOOLEAN;
BEGIN
    -- Obtener información del post
    SELECT * INTO post_record FROM Post_Foro WHERE id_post = p_id_post;
    
    -- Verificar si el votante es socio
    SELECT EXISTS (SELECT 1 FROM Socio WHERE dni = p_dni_votante) INTO es_socio;
    
    IF NOT es_socio THEN
        RAISE EXCEPTION 'Solo los socios pueden votar';
    END IF;
    
    -- Procesar según el tipo
    IF post_record.tipo = 'votacion' THEN
        -- Implementar lógica simple de votación (usar contenido para almacenar votos)
        -- Formato: "Pregunta|votos_total,user1,user2,user3"
        IF post_record.contenido ~ ('\|' || p_dni_votante || ',') OR 
           post_record.contenido ~ ('\|' || p_dni_votante || '$') THEN
            RAISE EXCEPTION 'Ya has votado en esta votación';
        END IF;
        
        -- Actualizar conteo de votos
        UPDATE Post_Foro
        SET contenido = REGEXP_REPLACE(
            contenido, 
            '\|(\d+)(,.*)?$', 
            '|' || (COALESCE(SUBSTRING(contenido FROM '\|(\d+)')::INT, 0) + 1) || 
            COALESCE(SUBSTRING(contenido FROM '\|\d+(,.*)$'), '') || 
            ',' || p_dni_votante
        )
        WHERE id_post = p_id_post;
        
    ELSIF post_record.tipo = 'encuesta' THEN
        -- Implementar lógica simple de encuesta
        -- Formato: "Pregunta?|opcion1,opcion2,opcion3|user1:2,user2:1"
        IF p_opcion IS NULL THEN
            RAISE EXCEPTION 'Debes seleccionar una opción para la encuesta';
        END IF;
        
        -- Verificar voto previo
        IF post_record.contenido ~ ('\|.*' || p_dni_votante || ':\d') THEN
            RAISE EXCEPTION 'Ya has votado en esta encuesta';
        END IF;
        
        -- Actualizar votos de encuesta
        UPDATE Post_Foro
        SET contenido = CASE 
            WHEN contenido NOT LIKE '%|%|%' THEN 
                -- Primera votación
                contenido || '|' || p_dni_votante || ':' || p_opcion
            ELSE
                -- Votaciones posteriores
                contenido || ',' || p_dni_votante || ':' || p_opcion
            END
        WHERE id_post = p_id_post;
    ELSE
        RAISE EXCEPTION 'Este post no es una votación o encuesta';
    END IF;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION obtener_resultados(
    p_id_post INTEGER)
RETURNS JSON AS $$
DECLARE
    post_record RECORD;
    resultados JSON;
    partes TEXT[];
    opciones TEXT[];
    votos TEXT[];
    i INTEGER;
    conteo_opciones JSONB := '{}';
BEGIN
    SELECT * INTO post_record FROM Post_Foro WHERE id_post = p_id_post;
    
    IF post_record.tipo = 'votacion' THEN
        -- Procesar votación
        partes := STRING_TO_ARRAY(post_record.contenido, '|');
        IF array_length(partes, 1) >= 2 THEN
            resultados := JSON_BUILD_OBJECT(
                'pregunta', partes[1],
                'total_votos', COALESCE(partes[2]::INT, 0)
            );
        ELSE
            resultados := JSON_BUILD_OBJECT(
                'pregunta', post_record.contenido,
                'total_votos', 0
            );
        END IF;
        
    ELSIF post_record.tipo = 'encuesta' THEN
        -- Procesar encuesta
        partes := STRING_TO_ARRAY(post_record.contenido, '|');
        
        IF array_length(partes, 1) >= 2 THEN
            opciones := STRING_TO_ARRAY(partes[2], ',');
            
            -- Inicializar conteo
            FOR i IN 1..array_length(opciones, 1) LOOP
                conteo_opciones := jsonb_set(conteo_opciones, ARRAY[opciones[i]], '0');
            END LOOP;
            
            -- Contar votos si existen
            IF array_length(partes, 1) >= 3 THEN
                votos := STRING_TO_ARRAY(partes[3], ',');
                FOR i IN 1..array_length(votos, 1) LOOP
                    IF votos[i] ~ ':\d+$' THEN
                        conteo_opciones := jsonb_set(
                            conteo_opciones, 
                            ARRAY[SPLIT_PART(votos[i], ':', 2)], 
                            (COALESCE(conteo_opciones->>SPLIT_PART(votos[i], ':', 2), '0')::INT + 1)::TEXT::jsonb
                        );
                    END IF;
                END LOOP;
            END IF;
            
            resultados := JSON_BUILD_OBJECT(
                'pregunta', partes[1],
                'opciones', opciones,
                'votos', conteo_opciones
            );
        ELSE
            resultados := JSON_BUILD_OBJECT(
                'pregunta', post_record.contenido,
                'opciones', ARRAY[]::TEXT[],
                'votos', '{}'
            );
        END IF;
    ELSE
        RAISE EXCEPTION 'Este post no es una votación o encuesta';
    END IF;
    
    RETURN resultados;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION publicar_noticia(
    p_titular VARCHAR(200),
    p_imagen VARCHAR(255),
    p_contenido TEXT,
    p_categoria VARCHAR(50),
    p_dni_admin VARCHAR(9)
)
RETURNS INTEGER AS $$
DECLARE
    v_id_noticia INTEGER;
    v_es_admin BOOLEAN;
BEGIN
    -- Verificar si el usuario es administrador
    SELECT EXISTS (SELECT 1 FROM Administrador WHERE dni = p_dni_admin) INTO v_es_admin;
    
    IF NOT v_es_admin THEN
        RAISE EXCEPTION 'Solo los administradores pueden publicar noticias';
    END IF;
    
    -- Validar contenido mínimo
    IF p_contenido IS NULL OR LENGTH(TRIM(p_contenido)) < 50 THEN
        RAISE EXCEPTION 'El contenido debe tener al menos 50 caracteres';
    END IF;
    
    -- Insertar la noticia
    INSERT INTO Noticia (titular, imagen, contenido, categoria)
    VALUES (p_titular, p_imagen, p_contenido, p_categoria)
    RETURNING id_noticia INTO v_id_noticia;
    
    RETURN v_id_noticia;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION obtener_noticias_ordenadas(
    p_limit INTEGER DEFAULT 10,
    p_offset INTEGER DEFAULT 0
) RETURNS TABLE (
    id_noticia INTEGER,
    titular VARCHAR(200),
    imagen VARCHAR(255),
    categoria VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        n.id_noticia,
        n.titular,
        n.imagen,
        n.categoria
    FROM Noticia n
    ORDER BY n.id_noticia DESC  -- Ordenar por las más recientes (asumiendo que id_noticia es autoincremental)
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION obtener_noticia_detallada(
    p_id_noticia INTEGER
) RETURNS TABLE (
    id_noticia INTEGER,
    titular VARCHAR(200),
    imagen VARCHAR(255),
    contenido TEXT,
    categoria VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        n.id_noticia,
        n.titular,
        n.imagen,
        n.contenido,
        n.categoria
    FROM Noticia n
    WHERE n.id_noticia = p_id_noticia;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Noticia no encontrada';
    END IF;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION obtener_noticia_detallada(
    p_id_noticia INTEGER
) RETURNS TABLE (
    id_noticia INTEGER,
    titular VARCHAR(200),
    imagen VARCHAR(255),
    contenido TEXT,
    categoria VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        n.id_noticia,
        n.titular,
        n.imagen,
        n.contenido,
        n.categoria
    FROM Noticia n
    WHERE n.id_noticia = p_id_noticia;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Noticia no encontrada';
    END IF;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION obtener_noticias_por_categoria(
    p_categoria VARCHAR(50),
    p_limit INTEGER DEFAULT 10,
    p_offset INTEGER DEFAULT 0
) RETURNS TABLE (
    id_noticia INTEGER,
    titular VARCHAR(200),
    imagen VARCHAR(255)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        n.id_noticia,
        n.titular,
        n.imagen
    FROM Noticia n
    WHERE n.categoria = p_categoria
    ORDER BY n.id_noticia DESC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION obtener_noticias_recientes(
    p_limit INTEGER DEFAULT 3
) RETURNS TABLE (
    id_noticia INTEGER,
    titular VARCHAR(200),
    imagen VARCHAR(255),
    categoria VARCHAR(50)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        n.id_noticia,
        n.titular,
        n.imagen,
        n.categoria
    FROM Noticia n
    ORDER BY n.id_noticia DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION filtrar_noticias(
    p_categoria VARCHAR(50) DEFAULT NULL,
    p_desde DATE DEFAULT NULL,
    p_hasta DATE DEFAULT NULL,
    p_limit INTEGER DEFAULT 10,
    p_offset INTEGER DEFAULT 0
) RETURNS TABLE (
    id_noticia INTEGER,
    titular VARCHAR(200),
    imagen VARCHAR(255),
    categoria VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        n.id_noticia,
        n.titular,
        n.imagen,
        n.categoria
    FROM Noticia n
    WHERE 
        (p_categoria IS NULL OR n.categoria = p_categoria) AND
        (p_desde IS NULL OR n.id_noticia >= (SELECT MIN(id_noticia) FROM Noticia WHERE id_noticia >= EXTRACT(EPOCH FROM p_desde))) AND
        (p_hasta IS NULL OR n.id_noticia <= (SELECT MAX(id_noticia) FROM Noticia WHERE id_noticia <= EXTRACT(EPOCH FROM p_hasta)))
    ORDER BY n.id_noticia DESC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION editar_noticia(
    p_id_noticia INTEGER,
    p_titular VARCHAR(200),
    p_imagen VARCHAR(255),
    p_contenido TEXT,
    p_categoria VARCHAR(50),
    p_dni_admin VARCHAR(9)
)
RETURNS VOID AS $$
BEGIN
     -- Validar que el usuario sea administrador
    IF NOT EXISTS (SELECT 1 FROM Administrador WHERE dni = p_dni_admin)THEN
        RAISE EXCEPTION 'Solo los administradores pueden publicar noticias';
    END IF;
    
    -- Validar contenido mínimo
    IF LENGTH(p_contenido) < 50 THEN
        RAISE EXCEPTION 'El contenido debe tener al menos 50 caracteres';
    END IF;
    
    -- Actualizar la noticia
    UPDATE Noticia SET
        titular = p_titular,
        imagen = p_imagen,
        contenido = p_contenido,
        categoria = p_categoria
    WHERE id_noticia = p_id_noticia;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Noticia no encontrada';
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_noticia(
    p_id_noticia INTEGER,
    p_dni_admin VARCHAR(9)
) 
RETURNS VOID AS $$
BEGIN
    -- Validar que el usuario sea administrador
    IF NOT EXISTS (SELECT 1 FROM Administrador WHERE dni = p_dni_admin)THEN
        RAISE EXCEPTION 'Solo los administradores pueden publicar noticias';
    END IF;
    
    -- Eliminar la noticia
    DELETE FROM Noticia 
    WHERE id_noticia = p_id_noticia;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Noticia no encontrada';
    END IF;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION agregar_patrocinador(
  p_nombre VARCHAR(100),
  p_tipo VARCHAR(50),
  p_email VARCHAR(100),
  p_telefono VARCHAR(15),
  p_logo VARCHAR(255),
  p_fecha_inicio DATE
) 
RETURNS VOID AS $$
BEGIN
  INSERT INTO Patrocinador (nombre, tipo, email, telefono, logo, fecha_inicio)
  VALUES (p_nombre, p_tipo, p_email, p_telefono, p_logo, p_fecha_inicio);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_patrocinador(
  p_id_patrocinador INTEGER
) 
RETURNS VOID AS $$
BEGIN
  UPDATE Patrocinador 
  SET fecha_fin = CURRENT_DATE 
  WHERE id_patrocinador = p_id_patrocinador;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION modificar_patrocinador(
  p_id_patrocinador INTEGER,
  p_nombre VARCHAR(100),
  p_tipo VARCHAR(50),
  p_email VARCHAR(100),
  p_telefono VARCHAR(15),
  p_logo VARCHAR(255)
) 
RETURNS VOID AS $$
BEGIN
  UPDATE Patrocinador 
  SET 
    nombre = p_nombre,
    tipo = p_tipo,
    email = p_email,
    telefono = p_telefono,
    logo = p_logo
  WHERE id_patrocinador = p_id_patrocinador;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION obtener_patrocinadores(
    p_activos_only BOOLEAN DEFAULT TRUE
) 
RETURNS TABLE (
    id_patrocinador INTEGER,
    nombre VARCHAR(100),
    tipo VARCHAR(50),
    logo VARCHAR(255),
    fecha_inicio DATE,
    fecha_fin DATE
) AS $$
BEGIN
    IF p_activos_only THEN
        RETURN QUERY
        SELECT 
            p.id_patrocinador,
            p.nombre,
            p.tipo,
            p.logo,
            p.fecha_inicio,
            p.fecha_fin
        FROM Patrocinador p
        WHERE p.fecha_fin IS NULL OR p.fecha_fin >= CURRENT_DATE
        ORDER BY p.nombre;
    ELSE
        RETURN QUERY
        SELECT 
            p.id_patrocinador,
            p.nombre,
            p.tipo,
            p.logo,
            p.fecha_inicio,
            p.fecha_fin
        FROM Patrocinador p
        ORDER BY 
            CASE WHEN p.fecha_fin IS NULL OR p.fecha_fin >= CURRENT_DATE THEN 0 ELSE 1 END,
            p.nombre;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION obtener_directiva()
RETURNS TABLE (
    dni VARCHAR(9),
    nombre_completo TEXT,
    cargo VARCHAR(50),
    foto_perfil VARCHAR(255),
    telefono VARCHAR(15),
    email VARCHAR(100)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.dni,
        u.nombre || ' ' || u.apellidos AS nombre_completo,
        a.cargo,
        COALESCE(a.foto_perfil, u.foto_perfil) AS foto_perfil,
        u.telefono,
        u.email
    FROM Usuario u
    JOIN Administrador a ON u.dni = a.dni
    WHERE a.cargo IN (
        'Presidente', 
        'Vicepresidente', 
        'Secretario', 
        'Tesorero',
        'Director Deportivo',
        'Vocal'
    )
    ORDER BY 
        CASE a.cargo 
            WHEN 'Presidente' THEN 1
            WHEN 'Vicepresidente' THEN 2
            WHEN 'Secretario' THEN 3
            WHEN 'Tesorero' THEN 4
            WHEN 'Director Deportivo' THEN 5
            ELSE 6
        END,
        u.apellidos;
END;
$$ LANGUAGE plpgsql;
