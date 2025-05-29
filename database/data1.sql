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
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.usuario (dni, nombre, apellidos, telefono, fecha_nacimiento, email, contrasena) FROM stdin;
26520114X	Manuel	Vico Arboledas	632632632	2002-02-01	manuel@gmail.com	$2b$12$o8M/Nr5035ZLwj1Q/lVApu7576BvedTSHZSzTGsyeWgqqNzivS0ia
26520115B	Gabriel	Vico Arboledas	644886872	2003-02-02	gabriel.arboledas@gmail.com	$2b$12$wADGzFC0CPLURq4zuf0Ice295Sti1JftflO/2.kvV7kiWaRL1U6ti
26206969X	Manolo	Vico	654654654	1999-05-11	manolo@gmail.com	$2b$12$aT9xEaYWttDGNZjHkgnOmesiulTO11R3p0cAcYTA1wQlBpQNiJDS.
\.
