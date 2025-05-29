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
-- Data for Name: producto; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.producto (id_producto, nombre, descripcion, precio, stock, imagen) FROM stdin;
4	Chaquetón Oficial del Campillo del Río C.F.	Tallas: 4, 6, 8, 10, 12, 14, S, M, L, XL, XXL, 3XL	50.00	7	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748513121/cct0qow84ljsydzgzgh9.png
1	Bufanda Oficial del Campillo del Río C.F.		8.00	5	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748509238/s8oekpga5o3xr78yysel.png
3	Chandal Oficial del Campillo del Río C.F.	Tallas: 4, 6, 8, 10, 12, 14, S, M, L, XL, XXL, 3XL	40.00	0	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748513046/pqjqvzaetx0rfjbk4nux.png
2	1ª Equipación Oficial del Campillo del Río C.F.	Tallas: 4, 6, 8, 10, 12, 14, S, M, L, XL, XXL, 3XL	28.00	0	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748513093/elrrmnvptj9zp9sdem9q.png
\.

