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
-- Data for Name: noticia; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.noticia (id_noticia, titular, imagen, contenido, categoria, dni_administrador) FROM stdin;
1	Bienvenidos a la nueva aplicación web del Campillo del Río C.F.	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748511565/owa9effm4hv6simt79dg.png	¡Estamos encantados de anunciar el lanzamiento de nuestra nueva aplicación web! Desde aquí podrás estar al día con las últimas noticias del club, consultar partidos, gestionar tus abonos y mucho más. ¡Gracias por ser parte de esta familia!	Noticias del Club	26520115B
3	ENTRENADOR 25-26 	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748511528/onvqjqjpkxya2om5aujc.png	Sergio Silva será el nuevo entrenador del Campillo del Río C.F. la próxima temporada.\nDespués de defender nuestros colores sobre el césped, ahora da un paso al frente para liderar desde el banquillo con la misma pasión, compromiso y entrega de siempre.\nPocos conocen este escudo como él, y estamos seguros de que lo dará todo en esta nueva etapa como míster.Un cambio importante, pero en casa y con los suyos.\n¡Mucha suerte en esta nueva etapa y bienvenido de nuevo a casa, Silva!	Senior Masculino	26520115B
4	COMUNICADO OFICIAL	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748511460/sihegp1cftrb9qdcrpns.png	El Campillo del Río C.F., su presidenta y su Junta Directiva quieren expresar su total apoyo a Andrés Pérez. Estamos profundamente conmovidos por lo ocurrido y le deseamos una pronta y completa recuperación.\nDesde el club, queremos trasladar nuestro cariño y fuerza a Andrés, así como a sus familiares y seres queridos en estos duros momentos. Sabemos que, con su fortaleza, superará esta situación y lo veremos pronto de vuelta.\nEl Campillo del Río C.F., sus compañeros de equipo, cuerpo técnico y la afición están contigo. ¡Te esperamos campeón!	Comunicados Oficiales	26520115B
2	¡GRACIAS LUIS CARLOS!	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748511502/hzry6z0fuenhvdbf4z4t.png	Esta mañana ya lo adelantaba @luis_carlos_rc en su perfil personal, y ahora nos toca a nosotros: gracias por estos tres años al frente del equipo. \nTres temporadas de entrega, compromiso y pasión, en las que no solo has sido entrenador, sino el pilar que ha hecho de este vestuario una auténtica familia.\n1 año: lleno de dificultades, donde nunca faltó el trabajo ni el esfuerzo.\n2 año: a un paso de los playoffs y unas semifinales de Copa Subdelegado épicas, dejando fuera a grandes equipos.\n3 año: lo conseguiste. Metiste al equipo en los playoffs y nos hiciste soñar con un ascenso a primera andaluza y aunque no pudo ser aún nos queda la Copa.\nGracias por dejar tu huella en el Campillo del Río C.F.\n¡Siempre serás uno de los nuestros, míster!	Senior Masculino	26520115B
\.

