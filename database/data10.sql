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
-- Data for Name: pedido_producto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pedido_producto (pedido_id, producto_id, id, cantidad) FROM stdin;
1	2	1	1
2	1	2	1
3	1	3	1
4	1	4	1
5	1	5	1
6	1	6	1
7	4	7	1
8	1	8	1
8	4	9	2
9	4	10	3
10	1	11	1
11	1	12	1
13	1	14	1
14	4	15	1
15	4	16	1
16	4	17	1
17	4	18	1
18	1	19	1
18	4	20	1
19	1	21	1
19	4	22	1
20	1	23	1
20	4	24	1
21	1	25	1
21	4	26	1
23	4	28	1
23	1	29	1
24	4	30	1
24	1	31	1
25	1	32	1
25	4	33	2
27	1	36	1
27	4	37	3
28	4	38	1
29	1	39	1
29	4	40	2
31	1	42	1
31	4	43	3
33	1	46	1
33	4	47	3
34	1	48	1
\.

