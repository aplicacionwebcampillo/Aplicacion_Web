--
-- PostgreSQL database dump
--

-- Dumped from database version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.2)
-- Dumped by pg_dump version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: actualizar_resultado_partido(character varying, character varying, character varying, character varying, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.actualizar_resultado_partido(p_nombre_competicion character varying, p_temporada character varying, p_local character varying, p_visitante character varying, p_resultado character varying)
    LANGUAGE plpgsql
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
$$;


--
-- Name: agregar_competicion(character varying, character varying, date, date, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.agregar_competicion(p_nombre character varying, p_temporada character varying, p_fecha_inicio date, p_fecha_fin date DEFAULT NULL::date, p_estado character varying DEFAULT 'pendiente'::character varying)
    LANGUAGE plpgsql
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
$$;


--
-- Name: agregar_jugador(integer, character varying, character varying, date, character varying, text); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.agregar_jugador(p_id_equipo integer, p_nombre character varying, p_posicion character varying, p_fecha_nacimiento date, p_foto character varying DEFAULT NULL::character varying, p_biografia text DEFAULT NULL::text)
    LANGUAGE plpgsql
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
$$;


--
-- Name: agregar_patrocinador(character varying, character varying, character varying, character varying, character varying, date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.agregar_patrocinador(p_nombre character varying, p_tipo character varying, p_email character varying, p_telefono character varying, p_logo character varying, p_fecha_inicio date) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  INSERT INTO Patrocinador (nombre, tipo, email, telefono, logo, fecha_inicio)
  VALUES (p_nombre, p_tipo, p_email, p_telefono, p_logo, p_fecha_inicio);
END;
$$;


--
-- Name: agregar_patrocinador(character varying, character varying, character varying, character varying, character varying, date, date, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.agregar_patrocinador(p_nombre character varying, p_tipo character varying, p_email character varying, p_telefono character varying, p_logo character varying, p_fecha_inicio date, p_fecha_fin date, p_dni_admin character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  INSERT INTO Patrocinador (nombre, tipo, email, telefono, logo, fecha_inicio, fecha_fin, dni_administrador)
  VALUES (p_nombre, p_tipo, p_email, p_telefono, p_logo, p_fecha_inicio, p_fecha_inicio, p_dni_admin);
END;
$$;


--
-- Name: agregar_producto(character varying, text, numeric, integer, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.agregar_producto(p_nombre character varying, p_descripcion text, p_precio numeric, p_stock integer, p_imagen character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO Producto (
        nombre, 
        descripcion, 
        precio, 
        stock, 
        imagen
    ) VALUES (
        p_nombre,
        p_descripcion,
        p_precio,
        p_stock,
        p_imagen
    );
END;
$$;


--
-- Name: aplicar_descuento_socio(numeric, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.aplicar_descuento_socio(p_precio_original numeric, p_dni_usuario character varying) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_descuento DECIMAL(10,2) := 0;
BEGIN
    IF EXISTS (SELECT 1 FROM Socio WHERE dni = p_dni_usuario) THEN
        v_descuento := p_precio_original * 0.10; -- 10% de descuento
    END IF;
    
    RETURN p_precio_original - v_descuento;
END;
$$;


--
-- Name: buscar_jugadores(character varying, character varying, integer, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.buscar_jugadores(nombre_busqueda character varying DEFAULT NULL::character varying, posicion_busqueda character varying DEFAULT NULL::character varying, edad_minima integer DEFAULT NULL::integer, edad_maxima integer DEFAULT NULL::integer, equipo_id integer DEFAULT NULL::integer, categoria_equipo character varying DEFAULT NULL::character varying) RETURNS TABLE(id_jugador integer, nombre character varying, posicion character varying, edad integer, equipo character varying, foto character varying)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: cancelar_abono(character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.cancelar_abono(p_dni_socio character varying)
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


--
-- Name: ceder_abono_temporal(character varying, character varying, date, date); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.ceder_abono_temporal(p_dni_cedente character varying, p_dni_beneficiario character varying, p_fecha_inicio date, p_fecha_fin date)
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


--
-- Name: comprar_abono(character varying, integer); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.comprar_abono(p_dni_socio character varying, p_id_abono integer)
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


--
-- Name: crear_encuesta(text, text, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.crear_encuesta(p_contenido text, p_opciones text, p_dni_autor character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: crear_post_foro(text, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.crear_post_foro(p_contenido text, p_tipo character varying, p_dni_usuario character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    nuevo_id INTEGER;
BEGIN
    -- Validar tipo de publicación
    IF p_tipo NOT IN ('discusion', 'encuesta', 'votacion') THEN
        RAISE EXCEPTION 'Tipo de publicación no válido';
    END IF;
    
    -- Insertar la nueva publicación
    INSERT INTO Post_Foro (contenido, tipo, dni_usuario)
    VALUES (p_contenido, p_tipo, p_dni_usuario)
    RETURNING id_post INTO nuevo_id;
    
    RETURN nuevo_id; 
END;
$$;


--
-- Name: crear_votacion(text, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.crear_votacion(p_contenido text, p_dni_autor character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: editar_noticia(integer, character varying, character varying, text, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.editar_noticia(p_id_noticia integer, p_titular character varying, p_imagen character varying, p_contenido text, p_categoria character varying, p_dni_admin character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: editar_post_foro(integer, text, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.editar_post_foro(p_id_post integer, p_nuevo_contenido text, p_dni_editor character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
    es_autor BOOLEAN;
    post_reportado BOOLEAN;
BEGIN
    -- Verificar si el editor es el autor original
    SELECT EXISTS (
        SELECT 1 FROM Autoria_Post
        WHERE id_post = p_id_post AND dni_usuario = p_dni_editor
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
$$;


--
-- Name: eliminar_administrador(character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.eliminar_administrador(p_dni character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: eliminar_competicion(character varying, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.eliminar_competicion(p_nombre character varying, p_temporada character varying)
    LANGUAGE plpgsql
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
$$;


--
-- Name: eliminar_jugador(integer); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.eliminar_jugador(p_id_jugador integer)
    LANGUAGE plpgsql
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
$$;


--
-- Name: eliminar_noticia(integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.eliminar_noticia(p_id_noticia integer, p_dni_admin character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: eliminar_patrocinador(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.eliminar_patrocinador(p_id_patrocinador integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  UPDATE Patrocinador 
  SET fecha_fin = CURRENT_DATE 
  WHERE id_patrocinador = p_id_patrocinador;
END;
$$;


--
-- Name: eliminar_post_foro(integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.eliminar_post_foro(p_id_post integer, p_dni_solicitante character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
    es_autor BOOLEAN;
    es_admin BOOLEAN;
BEGIN
    -- Verificar roles
    SELECT EXISTS (
        SELECT 1 FROM post_foro
        WHERE id_post = p_id_post AND dni_usuario = p_dni_solicitante
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
$$;


--
-- Name: eliminar_producto(integer); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.eliminar_producto(p_id_producto integer)
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


--
-- Name: eliminar_usuario(character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.eliminar_usuario(p_dni character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: evitar_stock_negativo(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.evitar_stock_negativo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.stock < 0 THEN
        RAISE EXCEPTION 'No se puede tener stock negativo para ningún producto';
    END IF;
    RETURN NEW;
END;
$$;


--
-- Name: filtrar_noticias(character varying, date, date, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.filtrar_noticias(p_categoria character varying DEFAULT NULL::character varying, p_desde date DEFAULT NULL::date, p_hasta date DEFAULT NULL::date, p_limit integer DEFAULT 10, p_offset integer DEFAULT 0) RETURNS TABLE(id_noticia integer, titular character varying, imagen character varying, categoria character varying)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: moderar_post(integer, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.moderar_post(p_id_post integer, p_dni_admin character varying, p_accion character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: modificar_administrador(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.modificar_administrador(p_dni character varying, p_nombre character varying DEFAULT NULL::character varying, p_apellidos character varying DEFAULT NULL::character varying, p_telefono character varying DEFAULT NULL::character varying, p_email character varying DEFAULT NULL::character varying, p_contrasena character varying DEFAULT NULL::character varying, p_cargo character varying DEFAULT NULL::character varying, p_permisos character varying DEFAULT NULL::character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Actualizar datos en Usuario
    UPDATE Usuario SET
        nombre = COALESCE(p_nombre, nombre),
        apellidos = COALESCE(p_apellidos, apellidos),
        telefono = COALESCE(p_telefono, telefono),
        email = COALESCE(p_email, email),
        contrasena = CASE 
                        WHEN p_contrasena IS NOT NULL THEN crypt(p_contrasena, gen_salt('bf'))
                        ELSE contrasena 
                     END
    WHERE dni = p_dni;
    
    -- Actualizar datos específicos en Administrador
    UPDATE Administrador SET
        cargo = COALESCE(p_cargo, cargo),
        permisos = COALESCE(p_permisos, permisos)
    WHERE dni = p_dni;
END;
$$;


--
-- Name: modificar_competicion(character varying, character varying, character varying, character varying, date, date, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.modificar_competicion(p_nombre_original character varying, p_temporada_original character varying, p_nuevo_nombre character varying DEFAULT NULL::character varying, p_nueva_temporada character varying DEFAULT NULL::character varying, p_nueva_fecha_inicio date DEFAULT NULL::date, p_nueva_fecha_fin date DEFAULT NULL::date, p_nuevo_estado character varying DEFAULT NULL::character varying)
    LANGUAGE plpgsql
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
$$;


--
-- Name: modificar_jugador(integer, integer, character varying, character varying, date, character varying, text); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.modificar_jugador(p_id_jugador integer, p_nuevo_id_equipo integer DEFAULT NULL::integer, p_nombre character varying DEFAULT NULL::character varying, p_posicion character varying DEFAULT NULL::character varying, p_fecha_nacimiento date DEFAULT NULL::date, p_foto character varying DEFAULT NULL::character varying, p_biografia text DEFAULT NULL::text)
    LANGUAGE plpgsql
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
$$;


--
-- Name: modificar_patrocinador(integer, character varying, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.modificar_patrocinador(p_id_patrocinador integer, p_nombre character varying, p_tipo character varying, p_email character varying, p_telefono character varying, p_logo character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: modificar_patrocinador(integer, character varying, character varying, character varying, character varying, character varying, date, date, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.modificar_patrocinador(p_id_patrocinador integer, p_nombre character varying, p_tipo character varying, p_email character varying, p_telefono character varying, p_logo character varying, p_fecha_inicio date, p_fecha_fin date, p_dni_admin character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  UPDATE Patrocinador 
  SET 
    nombre = p_nombre,
    tipo = p_tipo,
    email = p_email,
    telefono = p_telefono,
    logo = p_logo,
    fecha_inicio = p_fecha_inicio,
    fecha_fin = p_fecha_fin, 
    dni_administrador = p_dni_admin
  WHERE id_patrocinador = p_id_patrocinador;
END;
$$;


--
-- Name: modificar_producto(integer, character varying, text, numeric, integer, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.modificar_producto(p_id_producto integer, p_nombre character varying DEFAULT NULL::character varying, p_descripcion text DEFAULT NULL::text, p_precio numeric DEFAULT NULL::numeric, p_stock integer DEFAULT NULL::integer, p_imagen character varying DEFAULT NULL::character varying)
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


--
-- Name: modificar_usuario(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.modificar_usuario(p_dni character varying, p_nombre character varying DEFAULT NULL::character varying, p_apellidos character varying DEFAULT NULL::character varying, p_telefono character varying DEFAULT NULL::character varying, p_email character varying DEFAULT NULL::character varying, p_contrasena character varying DEFAULT NULL::character varying, p_tipo_membresia character varying DEFAULT NULL::character varying, p_foto_perfil character varying DEFAULT NULL::character varying, p_estado character varying DEFAULT NULL::character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
        contrasena = CASE 
                        WHEN p_contrasena IS NOT NULL THEN crypt(p_contrasena, gen_salt('bf'))
                        ELSE contrasena 
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
$$;


--
-- Name: obtener_calendario_partidos(character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_calendario_partidos(p_nombre_competicion character varying, p_temporada character varying) RETURNS TABLE(local character varying, visitante character varying, dia date, hora time without time zone, estadio character varying, resultado character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT p.local, p.visitante, p.dia, p.hora, p.estadio, p.resultado
    FROM Partido p
    WHERE p.nombre_competicion = p_nombre_competicion
    AND p.temporada_competicion = p_temporada
    ORDER BY p.dia, p.hora;
END;
$$;


--
-- Name: obtener_detalle_partido(character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_detalle_partido(p_nombre_competicion character varying, p_temporada character varying, p_local character varying, p_visitante character varying) RETURNS TABLE(competicion character varying, temporada character varying, fecha date, hora time without time zone, estadio character varying, resultado character varying)
    LANGUAGE plpgsql
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
$$;


--
-- Name: obtener_directiva(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_directiva() RETURNS TABLE(dni character varying, nombre_completo text, cargo character varying, foto_perfil character varying, telefono character varying, email character varying)
    LANGUAGE plpgsql
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
$$;


--
-- Name: obtener_historial_abonos(character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_historial_abonos(p_dni_socio character varying) RETURNS TABLE(temporada character varying, fecha_compra date, precio numeric, estado character varying, fecha_inicio date, fecha_fin date)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: obtener_noticia_detallada(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_noticia_detallada(p_id_noticia integer) RETURNS TABLE(id_noticia integer, titular character varying, imagen character varying, contenido text, categoria character varying)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: obtener_noticias_ordenadas(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_noticias_ordenadas(p_limit integer DEFAULT 10, p_offset integer DEFAULT 0) RETURNS TABLE(id_noticia integer, titular character varying, imagen character varying, categoria character varying)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: obtener_noticias_por_categoria(character varying, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_noticias_por_categoria(p_categoria character varying, p_limit integer DEFAULT 10, p_offset integer DEFAULT 0) RETURNS TABLE(id_noticia integer, titular character varying, imagen character varying)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: obtener_noticias_recientes(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_noticias_recientes(p_limit integer DEFAULT 3) RETURNS TABLE(id_noticia integer, titular character varying, imagen character varying, categoria character varying)
    LANGUAGE plpgsql
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
$$;


--
-- Name: obtener_patrocinadores(boolean); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_patrocinadores(p_activos_only boolean DEFAULT true) RETURNS TABLE(id_patrocinador integer, nombre character varying, tipo character varying, logo character varying, fecha_inicio date, fecha_fin date)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: obtener_plantilla_completa(character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_plantilla_completa(categoria_equipo character varying) RETURNS TABLE(id_jugador integer, nombre_jugador character varying, posicion character varying, edad integer, foto character varying, biografia text)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: obtener_resultados(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.obtener_resultados(p_id_post integer) RETURNS json
    LANGUAGE plpgsql
    AS $_$
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
$_$;


--
-- Name: publicar_noticia(character varying, character varying, text, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.publicar_noticia(p_titular character varying, p_imagen character varying, p_contenido text, p_categoria character varying, p_dni_admin character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
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
    INSERT INTO Noticia (titular, imagen, contenido, categoria, dni_administrador)
    VALUES (p_titular, p_imagen, p_contenido, p_categoria, p_dni_admin)
    RETURNING id_noticia INTO v_id_noticia;
    
    RETURN v_id_noticia;
END;
$$;


--
-- Name: registrar_administrador(character varying, character varying, character varying, character varying, date, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.registrar_administrador(p_dni character varying, p_nombre character varying, p_apellidos character varying, p_telefono character varying, p_fecha_nacimiento date, p_email character varying, p_contrasena character varying, p_cargo character varying, p_permisos character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Insertar en tabla Usuario
    INSERT INTO Usuario (dni, nombre, apellidos, telefono, fecha_nacimiento, email, contrasena)
    VALUES (p_dni, p_nombre, p_apellidos, p_telefono, p_fecha_nacimiento, p_email, p_contrasena);
    
    -- Insertar en tabla Administrador
    INSERT INTO Administrador (dni, cargo, permisos, estado)
    VALUES (p_dni, p_cargo, p_permisos, 'activo');
END;
$$;


--
-- Name: registrar_socio(character varying, character varying, character varying, character varying, date, character varying, character varying, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.registrar_socio(p_dni character varying, p_nombre character varying, p_apellidos character varying, p_telefono character varying, p_fecha_nacimiento date, p_email character varying, p_contrasena character varying, p_tipo_membresia character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_num_socio VARCHAR(20);
    v_ultimo_num INTEGER;
BEGIN
    -- Insertar en tabla Usuario primero
    IF NOT EXISTS (SELECT 1 FROM Usuario WHERE dni = p_dni) THEN
    	INSERT INTO Usuario(dni, nombre, apellidos, telefono, fecha_nacimiento, email, contrasena)
    	VALUES (p_dni, p_nombre, p_apellidos, p_telefono, p_fecha_nacimiento, p_email, p_contrasena);
    END IF;
    
    -- Generar número de socio único
    SELECT COALESCE(MAX(CAST(SUBSTRING(num_socio FROM 5) AS INTEGER)), 0)
    INTO v_ultimo_num
    FROM Socio;

    v_num_socio := 'SOC-' || LPAD((v_ultimo_num + 1)::TEXT, 3, '0');
    
    -- Insertar en tabla Socio
    INSERT INTO Socio(dni, num_socio, tipo_membresia)
    VALUES (p_dni, v_num_socio, p_tipo_membresia);
        
END;
$$;


--
-- Name: registrar_usuario(character varying, character varying, character varying, character varying, date, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.registrar_usuario(p_dni character varying, p_nombre character varying, p_apellidos character varying, p_telefono character varying, p_fecha_nacimiento date, p_email character varying, p_contrasena character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Insertar en tabla Usuario
    INSERT INTO Usuario (dni, nombre, apellidos, telefono, fecha_nacimiento, email, contrasena)
    VALUES (p_dni, p_nombre, p_apellidos, p_telefono, p_fecha_nacimiento, p_email, p_contrasena);
    
END;
$$;


--
-- Name: registrar_voto(integer, character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.registrar_voto(p_id_post integer, p_dni_votante character varying, p_opcion integer DEFAULT NULL::integer) RETURNS boolean
    LANGUAGE plpgsql
    AS $_$
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
$_$;


--
-- Name: renovar_abono(character varying, integer); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.renovar_abono(p_dni_socio character varying, p_id_abono_nuevo integer)
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


--
-- Name: reportar_post(integer, character varying, text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.reportar_post(p_id_post integer, p_dni_reporter character varying, p_motivo text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Marcar post como reportado
    UPDATE Post_Foro SET moderado = TRUE WHERE id_post = p_id_post;
END;
$$;


--
-- Name: validar_beneficiario_cesion(character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_beneficiario_cesion(p_dni character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: validar_categoria_noticia(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_categoria_noticia() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Lista de categorías predefinidas válidas
    IF NEW.categoria NOT IN (
        'Senior Masculino',
        'Senior Femenino',  
        'Cantera', 
        'Noticias del Club',
        'Comunicados Oficiales',
        'Actividades Sociales'
    ) THEN
        RAISE EXCEPTION 'La categoría "%" no es válida. Categorías permitidas: "Senior Masculino", "Senior Masculino", "Cantera", "Noticias del Club", "Comunicados Oficiales", "Actividades Sociales"', 
        NEW.categoria;
    END IF;
    
    RETURN NEW;
END;
$$;


--
-- Name: validar_cesion_abono(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_cesion_abono() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    abono_activo_beneficiario BOOLEAN;
    es_socio_beneficiario BOOLEAN;
BEGIN
    -- Verificar que el beneficiario esté registrado
    SELECT EXISTS (
        SELECT 1 FROM Usuario
        WHERE dni = NEW.dni_beneficiario
    ) INTO es_socio_beneficiario;
    
    IF NOT es_socio_beneficiario THEN
        RAISE EXCEPTION 'El beneficiario con DNI % no está registrado', NEW.dni_beneficiario;
    END IF;
    
    -- Verificar que el beneficiario no tenga un abono activo
    SELECT EXISTS (
        SELECT 1 FROM Socio_Abono sa
        JOIN Abono a ON sa.id_abono = a.id_abono
        WHERE sa.dni = NEW.dni_beneficiario
        AND a.fecha_fin >= CURRENT_DATE
        AND sa.pagado = TRUE
    ) INTO abono_activo_beneficiario;
    
    IF abono_activo_beneficiario THEN
        RAISE EXCEPTION 'El beneficiario con DNI % ya tiene un abono activo', NEW.dni_beneficiario;
    END IF;
    
    RETURN NEW;
END;
$$;


--
-- Name: validar_compra_abono(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_compra_abono() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    abono_activo BOOLEAN;
BEGIN
    -- Verificar si el usuario ya tiene un abono activo
    SELECT EXISTS (
        SELECT 1 FROM Socio_Abono sa
        JOIN Abono a ON sa.id_abono = a.id_abono
        WHERE sa.dni = NEW.dni 
        AND a.fecha_fin >= CURRENT_DATE
        AND sa.pagado = TRUE
    ) INTO abono_activo;
    
    IF abono_activo THEN
        RAISE EXCEPTION 'El usuario ya tiene un abono activo';
    END IF;
    
    RETURN NEW;
END;
$$;


--
-- Name: validar_contrasena_usuario(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_contrasena_usuario() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
BEGIN
    IF NEW.contrasena !~ '^(?=.*[A-Za-z])(?=.*\d).{8,}$' THEN
        RAISE EXCEPTION 'La contraseña debe ser alfanumérica y tener más de 8 caracteres';
    END IF;
    RETURN NEW;
END;
$_$;


--
-- Name: validar_dni_usuario(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_dni_usuario() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
DECLARE
    letras_dni CHAR(23) := 'TRWAGMYFPDXBNJZSQVHLCKE';
    num_dni INTEGER;
    letra_calculada CHAR;
BEGIN
    IF NEW.dni !~ '^\d{8}[A-Za-z]$' THEN
        RAISE EXCEPTION 'El DNI debe tener 8 números y una letra';
    END IF;
    
    num_dni := SUBSTRING(NEW.dni FROM 1 FOR 8)::INTEGER;
    letra_calculada := UPPER(SUBSTRING(letras_dni FROM (num_dni % 23)+1 FOR 1));
    
    IF UPPER(SUBSTRING(NEW.dni FROM 9 FOR 1)) != letra_calculada THEN
        RAISE EXCEPTION 'La letra del DNI no es válida';
    END IF;
    
    RETURN NEW;
END;
$_$;


--
-- Name: validar_dorsal_unico(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_dorsal_unico() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    existe BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1
        FROM jugador
        WHERE id_equipo = NEW.id_equipo
          AND dorsal = NEW.dorsal
          AND id_jugador <> NEW.id_jugador
    ) INTO existe;

    IF existe THEN
        RAISE EXCEPTION 'Ya existe un jugador con el dorsal % en el equipo %', NEW.dorsal, NEW.id_equipo;
    END IF;

    RETURN NEW;
END;
$$;


--
-- Name: validar_edad_usuario(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_edad_usuario() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF AGE(NEW.fecha_nacimiento) < INTERVAL '12 years' THEN
        RAISE EXCEPTION 'El usuario debe tener al menos 12 años';
    END IF;
    IF AGE(NEW.fecha_nacimiento) > INTERVAL '110 years' THEN
        RAISE EXCEPTION 'La edad no puede superar los 110 años';
    END IF;
    RETURN NEW;
END;
$$;


--
-- Name: validar_edicion_publicacion(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_edicion_publicacion() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Solo el autor puede editar
    IF OLD.dni_usuario != NEW.dni_usuario THEN
        RAISE EXCEPTION 'Solo el autor puede editar la publicación';
    END IF;
    
    -- No se puede editar si ha sido reportada
    IF OLD.moderado = TRUE THEN
        RAISE EXCEPTION 'No se puede editar una publicación reportada';
    END IF;
    
    RETURN NEW;
END;
$$;


--
-- Name: validar_eliminacion_competicion(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_eliminacion_competicion() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    tiene_partidos BOOLEAN;
BEGIN
    -- Verificar si tiene partidos asociados
    SELECT EXISTS (
        SELECT 1 FROM Partido
        WHERE nombre_competicion = OLD.nombre
        AND temporada_competicion = OLD.temporada
    ) INTO tiene_partidos;
    
    IF tiene_partidos THEN
        RAISE EXCEPTION 'No se puede eliminar una competición que tiene partidos asociados';
    END IF;
    
    RETURN OLD;
END;
$$;


--
-- Name: validar_eliminacion_jugador(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_eliminacion_jugador() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    en_partido BOOLEAN;
BEGIN
    -- Verificar si el jugador está asociado a un partido actual
    SELECT EXISTS (
        SELECT 1
        FROM Partido p
        JOIN Jugador j ON (p.local = j.id_equipo::varchar OR p.visitante = j.id_equipo::varchar)
        WHERE j.id_jugador = OLD.id_jugador
    ) INTO en_partido;

    IF en_partido THEN
        RAISE EXCEPTION 'No se puede eliminar un jugador que participa en un partido';
    END IF;

    RETURN OLD;
END;
$$;


--
-- Name: validar_eliminacion_producto(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_eliminacion_producto() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    tiene_stock BOOLEAN;
    en_compra BOOLEAN;
BEGIN
    -- Verificar si el producto tiene stock
    IF OLD.stock > 0 THEN
        RAISE EXCEPTION 'No se puede eliminar un producto con stock disponible';
    END IF;
    
    -- Verificar si el producto está en una compra pendiente
    SELECT EXISTS (
        SELECT 1 FROM Pedido p
        JOIN Compra c ON p.id_pedido = c.id_pedido
        WHERE p.id_producto = OLD.id_producto
        AND c.pagado = FALSE
    ) INTO en_compra;
    
    IF en_compra THEN
        RAISE EXCEPTION 'No se puede eliminar un producto asociado a una compra pendiente';
    END IF;
    
    RETURN OLD;
END;
$$;


--
-- Name: validar_eliminacion_publicacion_simple(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_eliminacion_publicacion_simple() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    es_usuario BOOLEAN;
    es_administrador BOOLEAN;
BEGIN
    -- Verificar si el operador es el autor (asumiendo que pasas el DNI como parámetro)
    SELECT EXISTS (
        SELECT 1 
        FROM post_foro 
        WHERE id_post = OLD.id_post AND dni_usuario = TG_ARGV[0]
    ) INTO es_usuario;
    
    -- Verificar si el operador es administrador
    SELECT EXISTS (
        SELECT 1 
        FROM Administrador 
        WHERE dni = TG_ARGV[0]
    ) INTO es_administrador;
    
    RAISE NOTICE 'es_usuario: %, es_administrador: %', es_usuario, es_administrador;
    
    -- Permitir eliminación si es el autor (y el post no está moderado) o si es un administrador
    IF NOT ((es_usuario AND NOT OLD.moderado) OR es_administrador) THEN
        RAISE EXCEPTION 'Solo el usuario (si no está moderado) o un administrador pueden eliminar publicaciones';
    END IF;
    
    RETURN OLD;
END;
$$;


--
-- Name: validar_email_usuario(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_email_usuario() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
BEGIN
    IF NEW.email !~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$' THEN
        RAISE EXCEPTION 'El email no tiene un formato válido';
    END IF;
    RETURN NEW;
END;
$_$;


--
-- Name: validar_modificacion_competicion(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_modificacion_competicion() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    
    RETURN NEW;
END;
$$;


--
-- Name: validar_modificacion_jugador(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_modificacion_jugador() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    en_partido BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM Partido p
        JOIN Jugador j ON (p.local = j.id_equipo::text OR p.visitante = j.id_equipo::text)
        WHERE j.id_jugador = NEW.id_jugador
        AND p.dia = CURRENT_DATE
    ) INTO en_partido;

    IF en_partido THEN
        RAISE EXCEPTION 'No se puede modificar un jugador que está participando en un partido activo';
    END IF;

    RETURN NEW;
END;
$$;


--
-- Name: validar_modificacion_producto(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_modificacion_producto() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    en_compra BOOLEAN;
BEGIN
    -- Verificar si el producto está en una compra en proceso
    SELECT EXISTS (
        SELECT 1 FROM pedido_producto p
        JOIN Compra c ON p.pedido_id = c.id_pedido
        WHERE p.pedido_id = NEW.id_producto
        AND c.pagado = FALSE
    ) INTO en_compra;
    
    IF en_compra THEN
        RAISE EXCEPTION 'No se puede modificar un producto asociado a una compra en proceso';
    END IF;
    
    RETURN NEW;
END;
$$;


--
-- Name: validar_noticia(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_noticia() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Validar título
    IF NEW.titular IS NULL OR LENGTH(TRIM(NEW.titular)) = 0 THEN
        RAISE EXCEPTION 'El título de la noticia no puede estar vacío';
    END IF;
    
    IF LENGTH(NEW.titular) > 100 THEN
        RAISE EXCEPTION 'El título no puede superar los 100 caracteres';
    END IF;
    
    -- Validar contenido
    IF NEW.contenido IS NULL OR LENGTH(TRIM(NEW.contenido)) < 50 THEN
        RAISE EXCEPTION 'El contenido debe tener al menos 50 caracteres';
    END IF;
    
    RETURN NEW;
END;
$$;


--
-- Name: validar_publicacion_foro(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_publicacion_foro() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    publicaciones_pendientes INTEGER;
BEGIN
    -- Verificar si el usuario tiene publicaciones pendientes de moderación
    SELECT COUNT(*) 
    INTO publicaciones_pendientes
    FROM Post_Foro
    WHERE dni_usuario = NEW.dni_usuario
    AND moderado = FALSE;
    
    IF publicaciones_pendientes > 0 THEN
        RAISE EXCEPTION 'El usuario tiene publicaciones pendientes de moderación';
    END IF;
    
    RETURN NEW;
END;
$$;


--
-- Name: validar_renovacion_abono(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_renovacion_abono() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    dias_restantes INTEGER;
BEGIN
    -- Solo validar si el socio está intentando cambiar de abono (renovación)
    IF NEW.id_abono <> OLD.id_abono THEN
        SELECT (a.fecha_fin - CURRENT_DATE)
        INTO dias_restantes
        FROM Abono a
        WHERE a.id_abono = NEW.id_abono;
        
        IF dias_restantes > 30 THEN
            RAISE EXCEPTION 'Solo se puede renovar el abono en los últimos 30 días antes de su expiración';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;


--
-- Name: validar_rol_administrador(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_rol_administrador() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Lista de roles predefinidos válidos
    IF NEW.cargo NOT IN ('Administrador General', 'Administrador de Contenidos', 'Administrador de Sistemas') THEN
        RAISE EXCEPTION 'El rol "%" no es válido. Roles permitidos: "Administrador General", "Administrador de Contenidos", "Administrador de Sistemas"', NEW.cargo;
    END IF;
    
    RETURN NEW;
END;
$$;


--
-- Name: validar_telefono_usuario(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.validar_telefono_usuario() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
BEGIN
    -- Verificar que el teléfono tenga valor cuando se proporciona
    IF NEW.telefono IS NOT NULL THEN
        -- Validar formato básico de teléfono (9 dígitos para España)
        IF NEW.telefono !~ '^[+]?[0-9]{9,15}$' THEN
            RAISE EXCEPTION 'El teléfono "%" no tiene un formato válido.', NEW.telefono;
        END IF;
        
        -- Validar que el teléfono no esté duplicado (opcional, según requisitos)
        IF EXISTS (SELECT 1 FROM Usuario WHERE telefono = NEW.telefono AND dni != NEW.dni) THEN
            RAISE EXCEPTION 'El teléfono "%" ya está registrado en el sistema', NEW.telefono;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$_$;


--
-- Name: verificar_disponibilidad(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.verificar_disponibilidad(p_id_producto integer, p_cantidad integer) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_stock INTEGER;
BEGIN
    SELECT stock INTO v_stock 
    FROM Producto 
    WHERE id_producto = p_id_producto;
    
    RETURN v_stock >= p_cantidad;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: abono; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.abono (
    id_abono integer NOT NULL,
    temporada character varying(20) NOT NULL,
    precio numeric(10,2) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    descripcion text,
    CONSTRAINT fechas_validas CHECK ((fecha_fin > fecha_inicio))
);


--
-- Name: abono_id_abono_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.abono_id_abono_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: abono_id_abono_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.abono_id_abono_seq OWNED BY public.abono.id_abono;


--
-- Name: administrador; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administrador (
    dni character varying(9) NOT NULL,
    cargo character varying(50) NOT NULL,
    permisos character varying(50) NOT NULL,
    foto_perfil character varying(255),
    estado character varying(15) DEFAULT 'activo'::character varying,
    CONSTRAINT administrador_estado_check CHECK (((estado)::text = ANY ((ARRAY['activo'::character varying, 'inactivo'::character varying])::text[])))
);


--
-- Name: producto; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.producto (
    id_producto integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    precio numeric(10,2) NOT NULL,
    stock integer DEFAULT 0 NOT NULL,
    imagen character varying(255) NOT NULL
);


--
-- Name: catalogo_productos; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.catalogo_productos AS
 SELECT producto.id_producto,
    producto.nombre,
    producto.descripcion,
    producto.precio,
        CASE
            WHEN (producto.stock > 0) THEN 'Disponible'::text
            ELSE 'Agotado'::text
        END AS disponibilidad,
    producto.imagen
   FROM public.producto
  WHERE (producto.stock >= 0);


--
-- Name: cesion_abono; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cesion_abono (
    id_cesion integer NOT NULL,
    dni_cedente character varying(9) NOT NULL,
    dni_beneficiario character varying(9) NOT NULL,
    id_abono integer NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    fecha_cesion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cedente_beneficiario_diferentes CHECK (((dni_cedente)::text <> (dni_beneficiario)::text)),
    CONSTRAINT fechas_cesion_validas CHECK ((fecha_fin > fecha_inicio))
);


--
-- Name: cesion_abono_id_cesion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cesion_abono_id_cesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cesion_abono_id_cesion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cesion_abono_id_cesion_seq OWNED BY public.cesion_abono.id_cesion;


--
-- Name: clasificacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clasificacion (
    nombre_competicion character varying(100) NOT NULL,
    temporada_competicion character varying(20) NOT NULL,
    equipo character varying(100) NOT NULL,
    posicion integer NOT NULL,
    puntos integer NOT NULL
);


--
-- Name: competicion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.competicion (
    nombre character varying(100) NOT NULL,
    temporada character varying(20) NOT NULL,
    id_equipo integer,
    formato character varying(20),
    CONSTRAINT formato_valido CHECK (((formato)::text = ANY ((ARRAY['Liga'::character varying, 'Copa'::character varying])::text[])))
);


--
-- Name: compra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.compra (
    dni character varying(9) NOT NULL,
    id_pedido integer NOT NULL,
    fecha_compra date DEFAULT CURRENT_DATE NOT NULL,
    pagado boolean DEFAULT false
);


--
-- Name: equipo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.equipo (
    id_equipo integer NOT NULL,
    categoria character varying(50) NOT NULL,
    num_jugadores integer DEFAULT 0 NOT NULL
);


--
-- Name: equipo_id_equipo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.equipo_id_equipo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: equipo_id_equipo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.equipo_id_equipo_seq OWNED BY public.equipo.id_equipo;


--
-- Name: jugador; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.jugador (
    id_jugador integer NOT NULL,
    id_equipo integer NOT NULL,
    nombre character varying(100) NOT NULL,
    posicion character varying(50) NOT NULL,
    fecha_nacimiento date NOT NULL,
    foto character varying(255),
    biografia text,
    dorsal integer NOT NULL
);


--
-- Name: jugador_id_jugador_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.jugador_id_jugador_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: jugador_id_jugador_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.jugador_id_jugador_seq OWNED BY public.jugador.id_jugador;


--
-- Name: noticia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.noticia (
    id_noticia integer NOT NULL,
    titular character varying(200) NOT NULL,
    imagen character varying(255),
    contenido text NOT NULL,
    categoria character varying(50) NOT NULL,
    dni_administrador character varying(9)
);


--
-- Name: noticia_id_noticia_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.noticia_id_noticia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: noticia_id_noticia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.noticia_id_noticia_seq OWNED BY public.noticia.id_noticia;


--
-- Name: partido; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.partido (
    nombre_competicion character varying(100) NOT NULL,
    temporada_competicion character varying(20) NOT NULL,
    local character varying(100) NOT NULL,
    visitante character varying(100) NOT NULL,
    dia date NOT NULL,
    hora time without time zone NOT NULL,
    jornada character varying(50) NOT NULL,
    resultado_local integer,
    resultado_visitante integer,
    acta character varying(255)
);


--
-- Name: patrocinador; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.patrocinador (
    id_patrocinador integer NOT NULL,
    nombre character varying(100) NOT NULL,
    tipo character varying(50) NOT NULL,
    email character varying(100),
    telefono character varying(15),
    logo character varying(255) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date,
    dni_administrador character varying(9)
);


--
-- Name: patrocinador_id_patrocinador_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.patrocinador_id_patrocinador_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: patrocinador_id_patrocinador_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.patrocinador_id_patrocinador_seq OWNED BY public.patrocinador.id_patrocinador;


--
-- Name: pedido; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pedido (
    id_pedido integer NOT NULL,
    descuento numeric(10,2) DEFAULT 0.00,
    precio_total numeric(10,2) NOT NULL
);


--
-- Name: pedido_id_pedido_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pedido_id_pedido_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pedido_id_pedido_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pedido_id_pedido_seq OWNED BY public.pedido.id_pedido;


--
-- Name: pedido_producto; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pedido_producto (
    pedido_id integer NOT NULL,
    producto_id integer NOT NULL,
    id integer NOT NULL,
    cantidad integer DEFAULT 1
);


--
-- Name: pedido_producto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pedido_producto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pedido_producto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pedido_producto_id_seq OWNED BY public.pedido_producto.id;


--
-- Name: post_foro; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.post_foro (
    id_post integer NOT NULL,
    contenido text NOT NULL,
    moderado boolean DEFAULT false,
    tipo character varying(20) NOT NULL,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    dni_usuario character varying(9) NOT NULL,
    CONSTRAINT post_foro_tipo_check CHECK (((tipo)::text = ANY ((ARRAY['discusion'::character varying, 'encuesta'::character varying, 'votacion'::character varying])::text[])))
);


--
-- Name: post_foro_id_post_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.post_foro_id_post_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: post_foro_id_post_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.post_foro_id_post_seq OWNED BY public.post_foro.id_post;


--
-- Name: predice; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.predice (
    dni character varying(9) NOT NULL,
    nombre_competicion character varying(100) NOT NULL,
    temporada_competicion character varying(20) NOT NULL,
    local character varying(100) NOT NULL,
    visitante character varying(100) NOT NULL,
    pagado boolean DEFAULT false,
    resultado_local integer NOT NULL,
    resultado_visitante integer NOT NULL
);


--
-- Name: producto_id_producto_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.producto_id_producto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: producto_id_producto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.producto_id_producto_seq OWNED BY public.producto.id_producto;


--
-- Name: socio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.socio (
    dni character varying(9) NOT NULL,
    num_socio character varying(20) NOT NULL,
    foto_perfil character varying(255),
    tipo_membresia character varying(30) NOT NULL,
    estado character varying(15) DEFAULT 'activo'::character varying,
    CONSTRAINT socio_estado_check CHECK (((estado)::text = ANY ((ARRAY['activo'::character varying, 'inactivo'::character varying, 'suspendido'::character varying])::text[])))
);


--
-- Name: socio_abono; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.socio_abono (
    dni character varying(9) NOT NULL,
    id_abono integer NOT NULL,
    fecha_compra date DEFAULT CURRENT_DATE NOT NULL,
    pagado boolean DEFAULT false
);


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuario (
    dni character varying(9) NOT NULL,
    nombre character varying(50) NOT NULL,
    apellidos character varying(100) NOT NULL,
    telefono character varying(15),
    fecha_nacimiento date NOT NULL,
    email character varying(100) NOT NULL,
    contrasena character varying(255) NOT NULL
);


--
-- Name: abono id_abono; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.abono ALTER COLUMN id_abono SET DEFAULT nextval('public.abono_id_abono_seq'::regclass);


--
-- Name: cesion_abono id_cesion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono ALTER COLUMN id_cesion SET DEFAULT nextval('public.cesion_abono_id_cesion_seq'::regclass);


--
-- Name: equipo id_equipo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.equipo ALTER COLUMN id_equipo SET DEFAULT nextval('public.equipo_id_equipo_seq'::regclass);


--
-- Name: jugador id_jugador; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jugador ALTER COLUMN id_jugador SET DEFAULT nextval('public.jugador_id_jugador_seq'::regclass);


--
-- Name: noticia id_noticia; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.noticia ALTER COLUMN id_noticia SET DEFAULT nextval('public.noticia_id_noticia_seq'::regclass);


--
-- Name: patrocinador id_patrocinador; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patrocinador ALTER COLUMN id_patrocinador SET DEFAULT nextval('public.patrocinador_id_patrocinador_seq'::regclass);


--
-- Name: pedido id_pedido; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido ALTER COLUMN id_pedido SET DEFAULT nextval('public.pedido_id_pedido_seq'::regclass);


--
-- Name: pedido_producto id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_producto ALTER COLUMN id SET DEFAULT nextval('public.pedido_producto_id_seq'::regclass);


--
-- Name: post_foro id_post; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_foro ALTER COLUMN id_post SET DEFAULT nextval('public.post_foro_id_post_seq'::regclass);


--
-- Name: producto id_producto; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto ALTER COLUMN id_producto SET DEFAULT nextval('public.producto_id_producto_seq'::regclass);


--
-- Name: abono abono_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.abono
    ADD CONSTRAINT abono_pkey PRIMARY KEY (id_abono);


--
-- Name: administrador administrador_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_pkey PRIMARY KEY (dni);


--
-- Name: cesion_abono cesion_abono_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono
    ADD CONSTRAINT cesion_abono_pkey PRIMARY KEY (id_cesion);


--
-- Name: clasificacion clasificacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clasificacion
    ADD CONSTRAINT clasificacion_pkey PRIMARY KEY (nombre_competicion, temporada_competicion, equipo);


--
-- Name: competicion competicion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competicion
    ADD CONSTRAINT competicion_pkey PRIMARY KEY (nombre, temporada);


--
-- Name: compra compra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_pkey PRIMARY KEY (dni, id_pedido);


--
-- Name: equipo equipo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.equipo
    ADD CONSTRAINT equipo_pkey PRIMARY KEY (id_equipo);


--
-- Name: jugador jugador_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT jugador_pkey PRIMARY KEY (id_jugador, id_equipo);


--
-- Name: noticia noticia_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.noticia
    ADD CONSTRAINT noticia_pkey PRIMARY KEY (id_noticia);


--
-- Name: noticia noticia_titular_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.noticia
    ADD CONSTRAINT noticia_titular_key UNIQUE (titular);


--
-- Name: partido partido_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_pkey PRIMARY KEY (nombre_competicion, temporada_competicion, local, visitante);


--
-- Name: patrocinador patrocinador_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patrocinador
    ADD CONSTRAINT patrocinador_pkey PRIMARY KEY (id_patrocinador);


--
-- Name: pedido pedido_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido
    ADD CONSTRAINT pedido_pkey PRIMARY KEY (id_pedido);


--
-- Name: pedido_producto pedido_producto_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_producto
    ADD CONSTRAINT pedido_producto_pkey PRIMARY KEY (id);


--
-- Name: post_foro post_foro_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_foro
    ADD CONSTRAINT post_foro_pkey PRIMARY KEY (id_post);


--
-- Name: predice predice_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.predice
    ADD CONSTRAINT predice_pkey PRIMARY KEY (dni, nombre_competicion, temporada_competicion, local, visitante, resultado_local, resultado_visitante);


--
-- Name: producto producto_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_nombre_key UNIQUE (nombre);


--
-- Name: producto producto_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_pkey PRIMARY KEY (id_producto);


--
-- Name: socio_abono socio_abono_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio_abono
    ADD CONSTRAINT socio_abono_pkey PRIMARY KEY (dni, id_abono);


--
-- Name: socio socio_num_socio_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio
    ADD CONSTRAINT socio_num_socio_key UNIQUE (num_socio);


--
-- Name: socio socio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio
    ADD CONSTRAINT socio_pkey PRIMARY KEY (dni);


--
-- Name: usuario usuario_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_email_key UNIQUE (email);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (dni);


--
-- Name: idx_jugador_equipo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_jugador_equipo ON public.jugador USING btree (nombre);


--
-- Name: idx_noticia_categoria; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_noticia_categoria ON public.noticia USING btree (categoria);


--
-- Name: idx_partido_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_partido_fecha ON public.partido USING btree (dia);


--
-- Name: idx_producto_categoria; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_producto_categoria ON public.producto USING btree (nombre);


--
-- Name: idx_socio_num_socio; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_socio_num_socio ON public.socio USING btree (dni);


--
-- Name: idx_usuario_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_usuario_email ON public.usuario USING btree (dni);


--
-- Name: producto trigger_evitar_stock_negativo; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_evitar_stock_negativo BEFORE UPDATE ON public.producto FOR EACH ROW EXECUTE FUNCTION public.evitar_stock_negativo();


--
-- Name: noticia trigger_validar_categoria_noticia; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_categoria_noticia BEFORE INSERT OR UPDATE OF categoria ON public.noticia FOR EACH ROW EXECUTE FUNCTION public.validar_categoria_noticia();


--
-- Name: cesion_abono trigger_validar_cesion_abono; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_cesion_abono BEFORE INSERT ON public.cesion_abono FOR EACH ROW EXECUTE FUNCTION public.validar_cesion_abono();


--
-- Name: socio_abono trigger_validar_compra_abono; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_compra_abono BEFORE INSERT ON public.socio_abono FOR EACH ROW EXECUTE FUNCTION public.validar_compra_abono();


--
-- Name: usuario trigger_validar_contrasena_usuario; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_contrasena_usuario BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_contrasena_usuario();


--
-- Name: usuario trigger_validar_dni; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_dni BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_dni_usuario();


--
-- Name: jugador trigger_validar_dorsal_unico; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_dorsal_unico BEFORE INSERT OR UPDATE ON public.jugador FOR EACH ROW EXECUTE FUNCTION public.validar_dorsal_unico();


--
-- Name: usuario trigger_validar_edad; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_edad BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_edad_usuario();


--
-- Name: post_foro trigger_validar_edicion_publicacion; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_edicion_publicacion BEFORE UPDATE ON public.post_foro FOR EACH ROW EXECUTE FUNCTION public.validar_edicion_publicacion();


--
-- Name: competicion trigger_validar_eliminacion_competicion; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_eliminacion_competicion BEFORE DELETE ON public.competicion FOR EACH ROW EXECUTE FUNCTION public.validar_eliminacion_competicion();


--
-- Name: jugador trigger_validar_eliminacion_jugador; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_eliminacion_jugador BEFORE DELETE ON public.jugador FOR EACH ROW EXECUTE FUNCTION public.validar_eliminacion_jugador();


--
-- Name: producto trigger_validar_eliminacion_producto; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_eliminacion_producto BEFORE DELETE ON public.producto FOR EACH ROW EXECUTE FUNCTION public.validar_eliminacion_producto();


--
-- Name: post_foro trigger_validar_eliminacion_publicacion_simple; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_eliminacion_publicacion_simple BEFORE DELETE ON public.post_foro FOR EACH ROW EXECUTE FUNCTION public.validar_eliminacion_publicacion_simple('current_user_dni');


--
-- Name: usuario trigger_validar_email_usuario; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_email_usuario BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_email_usuario();


--
-- Name: competicion trigger_validar_modificacion_competicion; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_modificacion_competicion BEFORE UPDATE ON public.competicion FOR EACH ROW EXECUTE FUNCTION public.validar_modificacion_competicion();


--
-- Name: jugador trigger_validar_modificacion_jugador; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_modificacion_jugador BEFORE UPDATE ON public.jugador FOR EACH ROW EXECUTE FUNCTION public.validar_modificacion_jugador();


--
-- Name: producto trigger_validar_modificacion_producto; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_modificacion_producto BEFORE UPDATE ON public.producto FOR EACH ROW EXECUTE FUNCTION public.validar_modificacion_producto();


--
-- Name: noticia trigger_validar_noticia; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_noticia BEFORE INSERT OR UPDATE ON public.noticia FOR EACH ROW EXECUTE FUNCTION public.validar_noticia();


--
-- Name: post_foro trigger_validar_publicacion_foro; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_publicacion_foro BEFORE INSERT ON public.post_foro FOR EACH ROW EXECUTE FUNCTION public.validar_publicacion_foro();


--
-- Name: socio_abono trigger_validar_renovacion_abono; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_renovacion_abono BEFORE UPDATE ON public.socio_abono FOR EACH ROW EXECUTE FUNCTION public.validar_renovacion_abono();


--
-- Name: administrador trigger_validar_rol_administrador; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_rol_administrador BEFORE INSERT OR UPDATE OF cargo ON public.administrador FOR EACH ROW EXECUTE FUNCTION public.validar_rol_administrador();


--
-- Name: usuario trigger_validar_telefono_usuario; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_telefono_usuario BEFORE INSERT OR UPDATE OF telefono ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_telefono_usuario();


--
-- Name: administrador administrador_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_dni_fkey FOREIGN KEY (dni) REFERENCES public.usuario(dni);


--
-- Name: cesion_abono cesion_abono_dni_beneficiario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono
    ADD CONSTRAINT cesion_abono_dni_beneficiario_fkey FOREIGN KEY (dni_beneficiario) REFERENCES public.usuario(dni);


--
-- Name: cesion_abono cesion_abono_dni_cedente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono
    ADD CONSTRAINT cesion_abono_dni_cedente_fkey FOREIGN KEY (dni_cedente) REFERENCES public.socio(dni);


--
-- Name: cesion_abono cesion_abono_id_abono_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono
    ADD CONSTRAINT cesion_abono_id_abono_fkey FOREIGN KEY (id_abono) REFERENCES public.abono(id_abono);


--
-- Name: clasificacion clasificacion_nombre_competicion_temporada_competicion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clasificacion
    ADD CONSTRAINT clasificacion_nombre_competicion_temporada_competicion_fkey FOREIGN KEY (nombre_competicion, temporada_competicion) REFERENCES public.competicion(nombre, temporada) ON DELETE CASCADE;


--
-- Name: competicion competicion_id_equipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competicion
    ADD CONSTRAINT competicion_id_equipo_fkey FOREIGN KEY (id_equipo) REFERENCES public.equipo(id_equipo) ON DELETE CASCADE;


--
-- Name: compra compra_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_dni_fkey FOREIGN KEY (dni) REFERENCES public.usuario(dni);


--
-- Name: compra compra_id_pedido_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_id_pedido_fkey FOREIGN KEY (id_pedido) REFERENCES public.pedido(id_pedido) ON DELETE RESTRICT;


--
-- Name: noticia fk_noticia_admin; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.noticia
    ADD CONSTRAINT fk_noticia_admin FOREIGN KEY (dni_administrador) REFERENCES public.administrador(dni);


--
-- Name: patrocinador fk_patrocinador_admin; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patrocinador
    ADD CONSTRAINT fk_patrocinador_admin FOREIGN KEY (dni_administrador) REFERENCES public.administrador(dni);


--
-- Name: post_foro fk_post_foro_usuario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_foro
    ADD CONSTRAINT fk_post_foro_usuario FOREIGN KEY (dni_usuario) REFERENCES public.usuario(dni) ON DELETE CASCADE;


--
-- Name: jugador jugador_id_equipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT jugador_id_equipo_fkey FOREIGN KEY (id_equipo) REFERENCES public.equipo(id_equipo) ON DELETE SET NULL;


--
-- Name: partido partido_nombre_competicion_temporada_competicion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_nombre_competicion_temporada_competicion_fkey FOREIGN KEY (nombre_competicion, temporada_competicion) REFERENCES public.competicion(nombre, temporada) ON DELETE CASCADE;


--
-- Name: pedido_producto pedido_producto_pedido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_producto
    ADD CONSTRAINT pedido_producto_pedido_id_fkey FOREIGN KEY (pedido_id) REFERENCES public.pedido(id_pedido) ON DELETE CASCADE;


--
-- Name: pedido_producto pedido_producto_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_producto
    ADD CONSTRAINT pedido_producto_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.producto(id_producto) ON DELETE CASCADE;


--
-- Name: predice predice_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.predice
    ADD CONSTRAINT predice_dni_fkey FOREIGN KEY (dni) REFERENCES public.socio(dni);


--
-- Name: predice predice_nombre_competicion_temporada_competicion_local_vis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.predice
    ADD CONSTRAINT predice_nombre_competicion_temporada_competicion_local_vis_fkey FOREIGN KEY (nombre_competicion, temporada_competicion, local, visitante) REFERENCES public.partido(nombre_competicion, temporada_competicion, local, visitante) ON DELETE CASCADE;


--
-- Name: socio_abono socio_abono_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio_abono
    ADD CONSTRAINT socio_abono_dni_fkey FOREIGN KEY (dni) REFERENCES public.socio(dni);


--
-- Name: socio_abono socio_abono_id_abono_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio_abono
    ADD CONSTRAINT socio_abono_id_abono_fkey FOREIGN KEY (id_abono) REFERENCES public.abono(id_abono) ON DELETE RESTRICT;


--
-- Name: socio socio_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio
    ADD CONSTRAINT socio_dni_fkey FOREIGN KEY (dni) REFERENCES public.usuario(dni);


--
-- Name: TABLE pedido_producto; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.pedido_producto TO admin_bd;


--
-- Name: SEQUENCE pedido_producto_id_seq; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,USAGE ON SEQUENCE public.pedido_producto_id_seq TO admin_bd;


--
-- PostgreSQL database dump complete
--

