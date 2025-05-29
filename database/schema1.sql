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
