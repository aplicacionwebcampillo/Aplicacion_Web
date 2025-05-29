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
-- Data for Name: abono; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.abono (id_abono, temporada, precio, fecha_inicio, fecha_fin, descripcion) FROM stdin;
1	Temporada 24-25	22.00	2024-09-01	2025-03-10	- Entrada a los 11 partidos de liga en casa.\n- Prioridad en el bus (partidos de larga distancia).\n- Descuento en los productos oficiales.\n- No incluye partidos de Copa.
\.
