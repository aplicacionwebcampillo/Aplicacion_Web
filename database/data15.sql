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
-- Data for Name: equipo; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.equipo (id_equipo, categoria, num_jugadores) FROM stdin;
1	Campillo del Río CF Senior	22
3	Campillo del Río CF Juvenil	22
2	Campillo del Río CF Femenino Senior	20
\.


