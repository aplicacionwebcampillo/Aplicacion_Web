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
-- Data for Name: partido; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.partido (nombre_competicion, temporada_competicion, local, visitante, dia, hora, jornada, resultado_local, resultado_visitante, acta) FROM stdin;
Fase Final 2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. TUCCITANA	2025-03-16	18:00:00	1ª Eliminatoria (Ida)	1	0	 
Fase Final 2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. TUCCITANA	C.D. CAMPILLO DEL RÍO C.F.	2025-03-23	19:15:00	1ª Eliminatoria (Vuelta)	5	2	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	ASOC.DVA. LOPERA	C.D. CAMPILLO DEL RÍO C.F.	2024-09-15	19:00:00	1	4	1	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	URGAVONA C.F.	2024-09-22	19:00:00	2	1	0	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	IBROS C.F.	2024-09-29	19:00:00	3	2	1	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	CLUB ATLETICO ARJONILLA	C.D. CAMPILLO DEL RÍO C.F.	2024-10-06	18:00:00	4	0	1	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	LINARES DEPORTIVO	2024-10-13	19:00:00	5	5	4	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	U.D. GUARROMAN	C.D. CAMPILLO DEL RÍO C.F.	2024-10-20	18:00:00	6	1	2	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	BAÑOS CLUB DEPORTIVO 2022	2024-10-27	18:00:00	7	1	2	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. JABALQUINTO	C.D. CAMPILLO DEL RÍO C.F.	2024-11-03	18:00:00	8	1	1	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	RECREATIVO DE BAILEN C.F.	2024-11-10	18:30:00	9	2	2	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. UTICA	C.D. CAMPILLO DEL RÍO C.F.	2024-11-17	19:00:00	10	3	1	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. LUPIÓN ATLÉTICO C.F.	2024-11-24	19:00:00	11	6	0	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	ASOC.DVA. LOPERA	2024-12-01	19:00:00	12	0	0	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	URGAVONA C.F.	C.D. CAMPILLO DEL RÍO C.F.	2024-12-15	19:00:00	13	1	1	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	IBROS C.F.	C.D. CAMPILLO DEL RÍO C.F.	2025-01-12	19:00:00	14	1	3	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	CLUB ATLETICO ARJONILLA	2025-01-19	19:00:00	15	2	0	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	LINARES DEPORTIVO	C.D. CAMPILLO DEL RÍO C.F.	2025-01-26	19:05:00	16	1	2	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	U.D. GUARROMAN	2025-02-02	19:00:00	17	2	0	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	BAÑOS CLUB DEPORTIVO 2022	C.D. CAMPILLO DEL RÍO C.F.	2025-02-09	19:00:00	18	2	3	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. JABALQUINTO	2025-02-16	18:00:00	19	2	1	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	RECREATIVO DE BAILEN C.F.	C.D. CAMPILLO DEL RÍO C.F.	2025-02-23	12:30:00	20	0	0	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. UTICA	2025-03-02	19:00:00	21	2	0	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. LUPIÓN ATLÉTICO C.F.	C.D. CAMPILLO DEL RÍO C.F.	2025-03-09	18:00:00	22	1	5	 
Copa Andalucía 2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. CASTELLAR IBERO	2024-08-28	00:00:00	Cuartos	0	3	 
Copa Andalucía 2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CASTELLAR IBERO	C.D. CAMPILLO DEL RÍO C.F.	2024-09-01	00:00:00	Cuartos	3	0	 
Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	LINARES DEPORTIVO	2025-04-02	20:30:00	2	1	0	 
Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	RECREATIVO DE BAILEN C.F.	2025-04-06	19:00:00	3	0	0	 
Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	LINARES DEPORTIVO	C.D. CAMPILLO DEL RÍO C.F.	2025-05-04	12:00:00	5	2	0	 
Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	RECREATIVO DE BAILEN C.F.	C.D. CAMPILLO DEL RÍO C.F.	2025-05-11	12:00:00	6	2	3	 
Fase Final Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. UBEDA VIVA	2025-05-18	20:30:00	Previa	1	2	 
Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	Descansa	2025-04-27	00:00:00	4	0	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	VILLARGORDO C.F.	2024-09-14	17:00:00	1	2	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	ATLETICO DE PORCUNA C.F.	C.D. CAMPILLO DEL RÍO C.F.	2024-09-21	19:30:00	2	0	3	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. ATLETICO MENGIBAR	2024-10-05	19:00:00	4	2	5	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	INTER DE JAEN C.F. "B"	C.D. CAMPILLO DEL RÍO C.F.	2024-10-27	16:00:00	5	2	3	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	RECREATIVO DE BAILEN C.F. "B"	2024-10-19	18:00:00	6	5	2	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	CLUB DEPORTIVO ANDUJAR F7-F11 MILANO	C.D. CAMPILLO DEL RÍO C.F.	2024-10-26	12:30:00	7	0	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	ASOC.DVA. LOPERA	2024-11-04	19:00:00	8	1	2	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	CLUB DEPORTIVO LONCHU "A"	C.D. CAMPILLO DEL RÍO C.F.	2024-11-09	18:00:00	9	1	8	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	URGAVONA C.F.	2024-12-11	20:00:00	10	2	1	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. LINARES CLUB DE FÚTBOL "B"	C.D. CAMPILLO DEL RÍO C.F.	2024-11-23	18:00:00	11	3	3	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. UTICA	2024-11-30	18:30:00	12	3	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	CLUB DEPORTIVO JAÉN F.C. "B"	C.D. CAMPILLO DEL RÍO C.F.	2024-12-14	20:00:00	13	1	1	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. TUCCITANA "B"	2024-12-28	18:00:00	14	4	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	U.D. GUARROMAN	C.D. CAMPILLO DEL RÍO C.F.	2025-01-11	19:00:00	15	5	1	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	VILLARGORDO C.F.	C.D. CAMPILLO DEL RÍO C.F.	2025-01-18	18:00:00	16	3	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	ATLETICO DE PORCUNA C.F.	2025-01-25	18:30:00	17	6	1	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	Descansa	2025-02-02	00:00:00	18	0	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. ATLETICO MENGIBAR	C.D. CAMPILLO DEL RÍO C.F.	2025-02-08	19:00:00	19	2	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	INTER DE JAEN C.F. "B"	2025-02-15	18:00:00	20	2	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	RECREATIVO DE BAILEN C.F. "B"	C.D. CAMPILLO DEL RÍO C.F.	2025-02-22	17:45:00	21	0	1	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	CLUB DEPORTIVO ANDUJAR F7-F11 MILANO	2025-03-02	00:00:00	22	0	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	ASOC.DVA. LOPERA	C.D. CAMPILLO DEL RÍO C.F.	2025-03-14	19:00:00	23	3	5	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	CLUB DEPORTIVO LONCHU "A"	2025-03-16	12:00:00	24	10	0	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	URGAVONA C.F.	C.D. CAMPILLO DEL RÍO C.F.	2025-03-22	19:00:00	25	2	1	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. LINARES CLUB DE FÚTBOL "B"	2025-03-29	18:00:00	26	1	2	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. UTICA	C.D. CAMPILLO DEL RÍO C.F.	2025-04-04	18:00:00	27	4	2	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	CLUB DEPORTIVO JAÉN F.C. "B"	2025-04-12	18:00:00	28	4	4	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. TUCCITANA "B"	C.D. CAMPILLO DEL RÍO C.F.	2025-04-26	20:00:00	29	3	2	 
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	U.D. GUARROMAN	2025-05-04	19:00:00	30	0	0	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	ATLETICO JIENNENSE F.C.F.	C.D. CAMPILLO DEL RÍO C.F.	2024-10-04	21:00:00	1	4	1	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	TORREPEROGIL C.D.	2024-10-20	18:00:00	2	6	0	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	LINARES DEPORTIVO	2024-11-03	12:00:00	3	2	1	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	REAL JAEN C.F., S.A.D. "B"	C.D. CAMPILLO DEL RÍO C.F.	2024-11-22	21:00:00	4	6	0	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. ALCALA ENJOY DESGUACES AUTOCOCHE	2024-12-01	16:45:00	5	0	7	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. UBEDA VIVA	C.D. CAMPILLO DEL RÍO C.F.	2024-12-28	17:00:00	6	4	0	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	MARTOS C.D.	2025-02-16	16:00:00	7	4	5	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	ATLETICO JIENNENSE F.C.F.	2025-01-19	17:15:00	8	0	5	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	TORREPEROGIL C.D.	C.D. CAMPILLO DEL RÍO C.F.	2025-02-01	11:00:00	9	2	4	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	LINARES DEPORTIVO	C.D. CAMPILLO DEL RÍO C.F.	2025-02-09	12:00:00	10	5	1	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	REAL JAEN C.F., S.A.D. "B"	2025-03-02	17:15:00	11	6	0	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. ALCALA ENJOY DESGUACES AUTOCOCHE	C.D. CAMPILLO DEL RÍO C.F.	2025-03-15	12:30:00	12	4	0	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	C.D. UBEDA VIVA	2025-04-25	20:30:00	13	1	1	 
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	MARTOS C.D.	C.D. CAMPILLO DEL RÍO C.F.	2025-05-10	11:30:00	14	4	1	 
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	LINARES DEPORTIVO B	2025-05-31	20:00:00	23	0	0	
\.


