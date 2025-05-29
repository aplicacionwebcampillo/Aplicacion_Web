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

--
-- Data for Name: administrador; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.administrador (dni, cargo, permisos, foto_perfil, estado) FROM stdin;
26520115B	Administrador de Sistemas	Administrador de Sistemas	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748458214/qkljd1ephkv8yb6ttyz2.png	activo
\.


--
-- Data for Name: socio; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.socio (dni, num_socio, foto_perfil, tipo_membresia, estado) FROM stdin;
26206969X	SOC-001	\N	anual	activo
26520115B	SOC-002	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748499781/ohgjlukjdix5uloxfmcf.png	anual	activo
\.

--
-- Data for Name: abono; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.abono (id_abono, temporada, precio, fecha_inicio, fecha_fin, descripcion) FROM stdin;
1	Temporada 24-25	22.00	2024-09-01	2025-03-10	- Entrada a los 11 partidos de liga en casa.\n- Prioridad en el bus (partidos de larga distancia).\n- Descuento en los productos oficiales.\n- No incluye partidos de Copa.
\.

--
-- Data for Name: socio_abono; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.socio_abono (dni, id_abono, fecha_compra, pagado) FROM stdin;
26206969X	1	2025-05-28	t
26520115B	1	2025-05-28	t
\.


--
-- Data for Name: cesion_abono; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.cesion_abono (id_cesion, dni_cedente, dni_beneficiario, id_abono, fecha_inicio, fecha_fin, fecha_cesion) FROM stdin;
\.

--
-- Data for Name: pedido; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.pedido (id_pedido, descuento, precio_total) FROM stdin;
1	0.00	0.00
2	0.00	8.00
3	0.00	8.00
4	0.00	8.00
5	0.00	8.00
6	0.00	8.00
7	0.00	50.00
8	0.00	108.00
9	0.00	150.00
10	0.00	8.00
11	0.00	8.00
12	0.00	8.00
13	0.00	8.00
14	0.00	50.00
15	0.00	50.00
16	0.00	50.00
17	0.00	50.00
18	0.00	58.00
19	0.00	58.00
20	0.00	58.00
21	0.00	58.00
22	0.00	58.00
23	0.00	58.00
24	0.00	58.00
25	0.00	108.00
26	0.00	158.00
27	0.00	158.00
28	0.00	50.00
29	0.00	108.00
30	0.00	108.00
31	0.00	158.00
32	0.00	158.00
33	0.00	158.00
34	0.25	6.00
\.

--
-- Data for Name: compra; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.compra (dni, id_pedido, fecha_compra, pagado) FROM stdin;
26520114X	6	2025-05-27	t
26520115B	7	2025-05-27	f
26520115B	9	2025-05-28	f
26520115B	10	2025-05-28	f
26520115B	11	2025-05-28	f
26520115B	13	2025-05-28	f
26520115B	14	2025-05-28	f
26520115B	15	2025-05-28	f
26520115B	16	2025-05-28	f
26520115B	17	2025-05-28	f
26520115B	18	2025-05-28	f
26520115B	19	2025-05-28	f
26520115B	20	2025-05-28	f
26520115B	21	2025-05-28	f
26520115B	23	2025-05-28	f
26520115B	25	2025-05-28	f
26520115B	33	2025-05-28	f
26520115B	8	2025-05-28	t
26520115B	34	2025-05-28	f
\.

--
-- Data for Name: producto; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.producto (id_producto, nombre, descripcion, precio, stock, imagen) FROM stdin;
4	Chaquetón Oficial del Campillo del Río C.F.	Tallas: 4, 6, 8, 10, 12, 14, S, M, L, XL, XXL, 3XL	50.00	7	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748513121/cct0qow84ljsydzgzgh9.png
1	Bufanda Oficial del Campillo del Río C.F.		8.00	5	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748509238/s8oekpga5o3xr78yysel.png
3	Chandal Oficial del Campillo del Río C.F.	Tallas: 4, 6, 8, 10, 12, 14, S, M, L, XL, XXL, 3XL	40.00	0	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748513046/pqjqvzaetx0rfjbk4nux.png
2	1ª Equipación Oficial del Campillo del Río C.F.	Tallas: 4, 6, 8, 10, 12, 14, S, M, L, XL, XXL, 3XL	28.00	0	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748513093/elrrmnvptj9zp9sdem9q.png
\.


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


--
-- Data for Name: noticia; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.noticia (id_noticia, titular, imagen, contenido, categoria, dni_administrador) FROM stdin;
1	Bienvenidos a la nueva aplicación web del Campillo del Río C.F.	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748511565/owa9effm4hv6simt79dg.png	¡Estamos encantados de anunciar el lanzamiento de nuestra nueva aplicación web! Desde aquí podrás estar al día con las últimas noticias del club, consultar partidos, gestionar tus abonos y mucho más. ¡Gracias por ser parte de esta familia!	Noticias del Club	26520115B
3	ENTRENADOR 25-26 	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748511528/onvqjqjpkxya2om5aujc.png	Sergio Silva será el nuevo entrenador del Campillo del Río C.F. la próxima temporada.\nDespués de defender nuestros colores sobre el césped, ahora da un paso al frente para liderar desde el banquillo con la misma pasión, compromiso y entrega de siempre.\nPocos conocen este escudo como él, y estamos seguros de que lo dará todo en esta nueva etapa como míster.Un cambio importante, pero en casa y con los suyos.\n¡Mucha suerte en esta nueva etapa y bienvenido de nuevo a casa, Silva!	Senior Masculino	26520115B
4	COMUNICADO OFICIAL	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748511460/sihegp1cftrb9qdcrpns.png	El Campillo del Río C.F., su presidenta y su Junta Directiva quieren expresar su total apoyo a Andrés Pérez. Estamos profundamente conmovidos por lo ocurrido y le deseamos una pronta y completa recuperación.\nDesde el club, queremos trasladar nuestro cariño y fuerza a Andrés, así como a sus familiares y seres queridos en estos duros momentos. Sabemos que, con su fortaleza, superará esta situación y lo veremos pronto de vuelta.\nEl Campillo del Río C.F., sus compañeros de equipo, cuerpo técnico y la afición están contigo. ¡Te esperamos campeón!	Comunicados Oficiales	26520115B
2	¡GRACIAS LUIS CARLOS!	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748511502/hzry6z0fuenhvdbf4z4t.png	Esta mañana ya lo adelantaba @luis_carlos_rc en su perfil personal, y ahora nos toca a nosotros: gracias por estos tres años al frente del equipo. \nTres temporadas de entrega, compromiso y pasión, en las que no solo has sido entrenador, sino el pilar que ha hecho de este vestuario una auténtica familia.\n1 año: lleno de dificultades, donde nunca faltó el trabajo ni el esfuerzo.\n2 año: a un paso de los playoffs y unas semifinales de Copa Subdelegado épicas, dejando fuera a grandes equipos.\n3 año: lo conseguiste. Metiste al equipo en los playoffs y nos hiciste soñar con un ascenso a primera andaluza y aunque no pudo ser aún nos queda la Copa.\nGracias por dejar tu huella en el Campillo del Río C.F.\n¡Siempre serás uno de los nuestros, míster!	Senior Masculino	26520115B
\.


--
-- Data for Name: post_foro; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.post_foro (id_post, contenido, moderado, tipo, fecha, dni_usuario) FROM stdin;
\.


--
-- Data for Name: patrocinador; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.patrocinador (id_patrocinador, nombre, tipo, email, telefono, logo, fecha_inicio, fecha_fin, dni_administrador) FROM stdin;
6	Hortícolas del Guadalquivir	Principal	 		https://res.cloudinary.com/dft3xbtrl/image/upload/v1748513885/wgtsaitfcxk0uzcvp4xc.png	2024-09-01	2024-09-01	26520115B
7	Caja Rural Jaén	Secundario	 		https://res.cloudinary.com/dft3xbtrl/image/upload/v1748513948/i0t1uqu6hu4ohfiiqfea.png	2024-09-01	2024-09-01	26520115B
3	Suzuki Garaje JJ	Principal	 		https://res.cloudinary.com/dft3xbtrl/image/upload/v1748514072/zoyffy95fzekmp0zb5cc.png	2024-09-01	2024-09-01	26520115B
8	KASTVLO Gimnasio	Secundario	 		https://res.cloudinary.com/dft3xbtrl/image/upload/v1748514186/b7te06ha4ua0ii4vbpp9.png	2024-09-01	2024-09-01	26520115B
9	MR SOUND	Secundario	 			2024-09-01	2024-09-01	26520115B
10	Materiales Pancorbo	Secundario	 			2024-09-01	2024-09-01	26520115B
11	El Hormiguero	Secundario	 			2024-09-01	2024-09-01	26520115B
12	Carnicería-Charcutería Pedro Romero	Secundario	 			2024-09-01	2024-09-01	26520115B
13	La Garza	Secundario	 			2024-09-01	2024-09-01	26520115B
14	El Canano	Secundario	 			2024-09-01	2024-09-01	26520115B
15	Pescadería MJ Ancla	Secundario	 			2024-09-01	2024-09-01	26520115B
16	Transportes MGJ	Secundario	 			2024-09-01	2024-09-01	26520115B
17	Ferretería El Goteron	Secundario	 			2024-09-01	2024-09-01	26520115B
18	Rufino	Secundario	 			2024-09-01	2024-09-01	26520115B
19	Casa Justo	Secundario	 			2024-09-01	2024-09-01	26520115B
20	Café-Bar La Codorniz	Secundario	 			2024-09-01	2024-09-01	26520115B
21	Durango	Secundario	 			2024-09-01	2024-09-01	26520115B
22	Bar Casa María	Secundario	 			2024-09-01	2024-09-01	26520115B
23	JOL LUX	Secundario	 			2024-09-01	2024-09-01	26520115B
24	petra	Secundario	 			2024-09-01	2024-09-01	26520115B
25	RiegoCamp	Secundario	 			2024-09-01	2024-09-01	26520115B
26	Alimentación Juan	Secundario	 			2024-09-01	2024-09-01	26520115B
27	CiCu	Secundario	 			2024-09-01	2024-09-01	26520115B
4	Alimentación Angel	Secundario	 			2024-09-01	2024-09-01	26520115B
5	Restaurante-Taberna Mirador de Cástulo	Secundario	 		https://res.cloudinary.com/dft3xbtrl/image/upload/v1748513860/unhzivvmqyba4joleprp.png	2024-09-01	2024-09-01	26520115B
28	SEX	Secundario	 			2024-09-01	2024-09-01	26520115B
29	COCI	Secundario	 			2024-09-01	2024-09-01	26520115B
30	Limpiezas LAFUENTE	Secundario	 			2024-09-01	2024-09-01	26520115B
31	Gámez Valderas	Secundario	 			2024-09-01	2024-09-01	26520115B
1	Ayuntamiento de Torreblascopedro y Campillo del Río	Principal			https://res.cloudinary.com/dft3xbtrl/image/upload/v1748514329/azjy6zthvwlcsccnutj4.png	2024-09-01	2024-09-01	26520115B
\.


--
-- Data for Name: equipo; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.equipo (id_equipo, categoria, num_jugadores) FROM stdin;
1	Campillo del Río CF Senior	22
3	Campillo del Río CF Juvenil	22
2	Campillo del Río CF Femenino Senior	20
\.


--
-- Data for Name: jugador; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.jugador (id_jugador, id_equipo, nombre, posicion, fecha_nacimiento, foto, biografia, dorsal) FROM stdin;
5	1	FRANCISCO JESÚS MUÑOZ GARCÍA	Delantero	1997-02-13		Un auténtico maestro del ataque, su incomparable visión de juego, velocidad y regate lo convierten en una pesadilla para las defensas rivales. Ya sea actuando como delantero, mediapunta o medio centro, su aportación en el juego ofensivo es crucial para generar ocasiones y goles. Estamos seguros de que seguirá cosechando éxitos y alegrías para nuestro equipo. ¡Muchísima suerte esta temporada Fran!	9
7	1	SERGIO BELTRAN BERRIO	Centrocampista	2004-11-23		Un jugador polivalente, capaz de brillar en cualquier posición del ataque, Sergio seguirá deleitándonos con su talento en el centro del campo una temporada más. Dotado de una excepcional visión de juego, es capaz de leer las jugadas a la perfección y distribuir balones con precisión quirúrgica. Posee un control de balón exquisito que le permite driblar rivales con facilidad y generar ocasiones de peligro en el área contraria. Un jugador de los que hacen disfrutar al público con su técnica depurada y visión de juego.	23
9	1	SERGIO TIRADO MARMOL	Defensa	1999-07-06		Un jugador con una gran proyección, que atesora unas cualidades técnicas y físicas excepcionales. Su amplia zancada le permite recorrer la banda con facilidad y rapidez, mientras que su dominio del juego aéreo lo convierte en un arma letal. Posee una excelente salida de balón, lo que le permite iniciar el ataque con fluidez y precisión. 	18
12	1	ROBERTO ORTEGA ORIHUELA	Defensa	1994-04-26		Un jugador curtido en mil batallas, que atesora una amplia experiencia futbolística y una humildad ejemplar dentro y fuera del campo. Su incansable recorrido por la banda lo convierte en un arma letal en ataque y defensa. Estamos seguros de que seguirá regalándonos momentos inolvidables en esta nueva temporada.	12
4	1	JUSTIN EMIL MARTINEZ JAVIER	Delantero	2003-12-22	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748498045/fn8xcvoasjzf1uarabzq.png	¡Justin regresa a Campillo tras su paso por el Begíjar C.F.! Con su increíble rapidez y una agilidad que desconcierta a cualquier defensa, Justin vuelve más preparado que nunca para hacer la diferencia en el campo. Su talento para el regate, sumado a su explosividad y precisión en cada movimiento, lo convierten en un jugador clave capaz de abrir espacios y generar oportunidades de gol tanto para él como para el equipo. La experiencia acumulada en el Begíjar C.F. le ha dado un plus de madurez e inteligencia futbolística que, junto a su habilidad para tomar decisiones bajo presión, refuerzan aún más su rol como extremo. Campillo recupera a un jugador con gran visión de juego, técnica exquisita y determinación para brillar. Sin duda, su regreso será una gran ventaja para el equipo y una pesadilla para los rivales. 	16
8	1	DAVID TIRADO MARMOL	Portero	2001-03-07	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748516388/uhv8fgr0xv2tbhrllinb.png	Su destreza, reflejos y gran capacidad de anticipación lo convierten en un auténtico muro impenetrable. Es una verdadera pesadilla para cualquier delantero. Además de sus habilidades técnicas, posee una presencia imponente en la portería. Su confianza y capacidad para comunicarse con sus compañeros le permiten organizar la defensa y mantener a raya las arremetidas enemigas.	1
16	1	GABRIEL MUÑOZ ROMERO	Centrocampista	2001-06-08		Gabri es un maestro del juego en el mediocentro. Su capacidad para interceptar pases, romper el juego rival y recuperar balones es incomparable. Su visión táctica excepcional y su agresividad controlada lo convierten en un jugador colosal para nuestro equipo. Un jugador inteligente que sabe leer el juego a la perfección y que siempre está un paso por delante del rival. Su precisión en los pases le permite iniciar los ataques con fluidez y efectividad, convirtiéndolo en un motor fundamental. Su presencia en el campo es invaluable. Un verdadero pilar en nuestro equipo que nos aporta confianza y seguridad. Un jugador imprescindible para nuestro equipo que siempre da el cien por cien en cada partido.	20
18	1	JUAN MANUEL TRUJILLO BLE	Delantero	2000-01-17		Juan es un futbolista camaleónico, capaz de adaptarse a cualquier posición ofensiva con maestría y solvencia. Su amplio recorrido por el campo le permite generar peligro en cualquier zona del ataque, mientras que su especialidad en el último pase lo convierte en un creador de ocasiones de gol de primer nivel. Su desequilibrio en el uno contra uno y su olfato goleador lo convierten en una amenaza constante para las defensas rivales. Su renovación es una gran noticia para nuestro club, ya que nos asegura contar con un jugador de gran talento y experiencia una temporada más.	7
21	1	ENRIQUE RODRIGUEZ RUIZ	Defensa	1996-11-24		El futbolista linarense, formado en la cantera del Linares Dptvo. donde llegó a jugar en Tercera División, llega procedente del Atco. Jaén. Kike es un central que nos aportará muchísima experiencia, tiene una gran salida de balón y un muy buen juego aéreo. 	14
23	1	CRISTIAN CORTES HERRANZ	Defensa	1987-03-30		Cristian no es solo un defensor excepcional, sino también un profesional intachable y un compañero ejemplar. Su dedicación inigualable al club y a sus compañeros lo convierten en una pieza fundamental de nuestro proyecto. Cristian es un muro infranqueable. Su habilidad para leer el juego y anticiparse a los movimientos de los delanteros rivales y cortar pases lo convierten en un baluarte en nuestra línea defensiva. Más allá de sus cualidades futbolísticas, Cristian es un jugador leal y comprometido con los valores del club. Su pasión por el fútbol y su entrega incondicional en cada partido lo convierten en un ejemplo a seguir. Su actitud positiva y su espíritu de equipo son fundamentales para crear un ambiente de trabajo óptimo dentro del vestuario. 	4
49	2	ANDREA OYA MORENO		2001-09-12		 	49
32	3	HUGO MARIN SERRANO		2006-02-17		 	32
1	1	JOSE LUIS PEREZ CRESPO		1988-02-02		Nuestro segunda capitán y cerrojo en la zaga seguirá un año más vistiendo la camiseta albiceleste. Jugador que va muy bien al corte y gracias a su complexión mejor aún en el juego aéreo, una pieza fundamental en nuestra defensa. Veteranía, humildad y liderazgo lo hacen un buen jugador en el campo y mejor aún en el vestuario.	22
2	1	CRISTOBAL MOYA CARMONA		1996-09-24		Se une al Campillo del Río C.F. desde el Linares Deportivo FS. Cambia así el parquet por el verde del Municipal. Cristóbal que ha llegado incluso a jugar en Segunda B en el filial del Jaén Paraíso Interior FS, viene de anotar 41 goles en su último club. Se incorpora para aportar una presencia ofensiva notable y una capacidad goleadora impresionante. Destaca por su velocidad y su agilidad, lo que le permite superar a los defensores y crear oportunidades de gol desde cualquier posición. Tiene una notable capacidad para posicionarse estratégicamente en el área, anticipándose a los movimientos del balón y de los defensores, lo que le permite aprovechar cualquier oportunidad de gol. Su determinación y tenacidad en el campo son ejemplares, luchando por cada balón y nunca dando una jugada por perdida. Esta actitud, junto con su capacidad para mantenerse calmado bajo presión, le permite rendir al máximo nivel en momentos cruciales	21
6	1	ALBERTO MARTINEZ SANCHO		2004-01-24		Alberto aportará su dedicación y esfuerzo para contribuir al éxito del equipo en esta nueva temporada. Su dominio de balón con ambas piernas nos seguirá regalando momentos de alegría y deleite durante esta nueva temporada. Este jugador tiene un futuro prometedor y estamos seguros de que nos brindará grandes satisfacciones tanto dentro como fuera del terreno de juego.	8
11	1	ALEJANDRO MARTINEZ FERNANDEZ		1997-01-25		Un líder indiscutible, Alex volverá a enfundarse el brazalete de capitán una temporada más. Un jugador ejemplar, reúne todas las cualidades de un futbolista: talento innato, astucia y una pasión arrolladora. Su agudeza para leer el juego y su capacidad de tomar decisiones certeras en milésimas lo convierten en un centrocampista excepcional. Con una visión de juego periférica y una precisión milimétrica en los pases, es capaz de conectar con cada uno de sus compañeros, tejiendo una verdadera sinfonía futbolística.\nSu compromiso inquebrantable y su dedicación lo han convertido en un líder nato. Su ejemplo inspirador motiva a sus compañeros a dar lo mejor de sí mismos en cada partido, sacando a relucir su máximo potencial. ¡Un verdadero privilegio contar con él como capitán!	10
13	1	PEDRO M MATEOS ARROYO		1987-09-20		Un jugador de espíritu incansable que nunca da un balón por perdido y lucha hasta el final. Es un valioso activo para nuestro conjunto. Un jugador que siempre está dispuesto a asumir responsabilidades y generar peligro en la portería rival.	11
14	1	MANUEL CASTILLO MONTAVEZ		1995-03-16		El futbolista natural de Linares, se ha formado en algunas de las mejores canteras de España. Llega procedente del Iliturgi 2016 CF, anteriormente jugó en Tercera División en equipos como Mancha Real, Huetor Tajar, Martos, Linares Dptvo. entre otros. Destaca por su potencia, técnica y su efectividad de cara a la portería. 	27
60	2	MARIA DEL MAR CUEVAS CEACERO		1993-07-31		 	60
61	2	MARTINA GIURBINO PLEGUEZUELOS		1998-04-09		 	61
62	2	MARIA GOMEZ GARRIDO		2001-07-06		 	62
63	2	JULIA RUIZ ARANDA		1992-02-01		 	63
64	2	ANA DE AMO PEREZ		1995-11-15		 	64
65	2	SORAYA CASTILLO LOPEZ		1991-05-04		 	65
15	1	JUAN GARCIA CHICA		1994-01-16		Un jugador que encarna a la perfección los valores de compromiso, entrega y sacrificio. Un guerrero incansable que se desvive por el equipo tanto dentro como fuera del campo. Carrasco es un competidor tenaz que no da un balón por perdido y que lucha hasta el final. Su actitud ejemplar y dedicación sin límites lo convierten en un referente para sus compañeros y un ejemplo a seguir para las nuevas generaciones. Sobre el césped es un defensor infranqueable que destaca por su disciplina táctica, su excelente lectura del juego y su imponente presencia física. Un muro inexpugnable que blinda nuestra portería y que transmite seguridad y confianza a todo el equipo. Mención muy especial a su amigo Juan Ble, quien fue un fiel seguidor de nuestro club y quien le inculcó los valores del deporte y la importancia de luchar siempre por los sueños, el te guiará una temporada más.	6
17	1	JUAN FRANCISCO MORAL MORENO		1997-02-11		El futbolista de Villargordo, formado en la cantera del Atco. Jaén y que llega procedente del Villargordo CF es un jugador de lo que no da un balón por perdido, muy dinámico, técnico y con carácter.	5
19	1	CRISTIAN GOMEZ MARTINEZ		2000-02-27		Un jugador que ha demostrado una visión del juego excepcional y una facilidad pasmosa para encontrar al compañero mejor posicionado. Su amplio repertorio de recursos técnicos le permite superar cualquier línea defensiva rival con precisión y fluidez. Su capacidad para leer el juego y tomar las decisiones correctas en cada momento le convierten en un jugador imprescindible para nuestro equipo.	19
20	1	VICTOR JIMENEZ GARCIA		2001-04-12		Un extremo vertiginoso, dueño de una velocidad arrolladora y un regate excelente, seguirá surcando la banda izquierda de nuestro equipo otra temporada más. Un auténtico peligro constante para las defensas rivales, su olfato goleador insaciable lo convierte en una amenaza constante en el área contraria. Su llegada a portería es un torbellino, capaz de desequilibrar cualquier partido en un abrir y cerrar de ojos. Es un jugador fundamental en nuestro esquema de juego.	17
22	1	ILDEFONSO ARBOLEDAS CUEVAS		2003-02-16		 @arcu_jr ficha por Campillo desde el C.D. Jabalquinto! Un jugador dinámico y veloz que domina la banda derecha con entrega total, luchando cada balón hasta el final. Estamos seguros que será una pieza clave en el equipo lo que resta de temporada. 	15
25	3	OSCAR POYATOS MOLINA		2006-03-30		 	25
26	3	ALVARO ALARCON SERRANO		2008-01-06		 	26
27	3	FRANCISCO AMADOR CASTILLO GONZALEZ		2006-10-10		 	27
28	3	ANGEL ANTONIO CASTILLO GONZALEZ		2006-10-10		 	28
29	3	FRANCISCO JESÚS COLON DÍAZ		2008-08-30		 	29
30	3	LORENZO LUJAN GARCIA		2008-05-15		 	30
31	3	ALFONSO BEDMAR QUESADA		2008-11-07		 	31
33	3	JOSE HINOJOSA MARTINEZ		2006-01-27		 	33
34	3	FRANCISCO QUESADA PEREZ		2006-01-24		 	34
35	3	RUBEN BURGALES PALACIOS		2008-06-22		 	35
36	3	SERGIO VALERO CRUZ		2006-10-27		 	36
37	3	ANGEL MOLINA FERNANDEZ		2006-02-01		 	37
38	3	VICTOR UCERO CEREZO		2006-11-02		 	38
39	3	YERAY GONZALEZ JIMENEZ		2007-08-23		 	39
40	3	FRANCISCO REQUENA MENDEZ		2006-09-03		 	40
41	3	YERAY GUTIERREZ JIMENEZ		2006-12-29		 	41
42	3	MANUEL REDONDO MARTINEZ		2006-01-06		 	42
43	3	OSCAR NAVARRO MARMOL		2008-01-29		 	43
44	3	ERNESTO MORENO SERRANO		2007-05-13		 	44
45	3	FERNANDO MORENO TORRES		2007-02-02		 	45
46	2	ROCIO MORENO MONTORO		2010-12-16		 	46
47	2	ALMUDENA MARTIN SIERRA		2009-07-25		 	47
48	2	RAQUEL MORENO CIVANTOS		2002-10-15		 	48
50	2	SILVIA MORAL VEGA		2001-09-12		 	50
51	2	MARIA TERESA CARRETERO GONZALEZ		1996-12-22		 	51
52	2	MARIA JOSE HOCES ARIAS		1994-08-31		 	52
53	2	ANA FERNANDEZ RAMOS		2011-04-07		 	53
54	2	MARIA JIMÉNEZ LÓPEZ		2004-04-30		 	54
55	2	OMAYMA FAGROUCH FAGROUCH		2004-11-20		 	55
56	2	YADIRA VANESSA SOTAMINGA CLAVON		1996-07-17		 	56
57	2	AURORA PADILLA COETO		1989-11-30		 	57
58	2	MARIA JOSE MORENO CIVANTOS		1997-04-30		 	58
59	2	MARTA DIAZ ALARCON		1998-10-26		 	59
24	3	ALEJANDRO RAMIREZ QUEVEDO		2006-02-04		 	24
10	1	RAUL SANTIAGO PALACIOS		1997-06-03	https://res.cloudinary.com/dft3xbtrl/image/upload/v1748516451/wpwaqub05fvw5yi1gkuz.png	Raúl es un auténtico portento físico y técnico, destaca por su increíble velocidad, fuerza y explosividad en el campo. Su capacidad para romper líneas con su potencia y arrancadas fulgurantes lo convierten en una amenaza constante para las defensas rivales.Con una visión de juego privilegiada, es capaz de leer cada situación con inteligencia y precisión, distribuyendo balones con criterio y generando ocasiones de peligro en cada encuentro. Su entrega y determinación lo han llevado a brillar en equipos como el C.D. Torreperogil, C.D. Navas, y más recientemente en el Begíjar C.F., donde dejó su huella con actuaciones memorables. 	2
\.


--
-- Data for Name: competicion; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.competicion (nombre, temporada, id_equipo, formato) FROM stdin;
Fase Final 2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	1	Copa
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	1	Liga
Copa Andalucía 2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	1	Copa
Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	1	Liga
Fase Final Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	1	Copa
Trofeo Copa Diputación Juvenil (Jaén)	Temporada 2024-2025	3	Copa
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	3	Liga
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	2	Liga
\.


--
-- Data for Name: clasificacion; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.clasificacion (nombre_competicion, temporada_competicion, equipo, posicion, puntos) FROM stdin;
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	LINARES DEPORTIVO	1	57
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	BAÑOS CLUB DEPORTIVO 2022	2	49
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. UTICA	4	42
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	URGAVONA C.F.	5	41
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	RECREATIVO DE BAILEN C.F.	6	31
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	ASOC.DVA. LOPERA	7	27
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. JABALQUINTO	8	26
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	IBROS C.F.	9	26
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	U.D. GUARROMAN	10	19
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	CLUB ATLETICO ARJONILLA	11	5
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. LUPIÓN ATLÉTICO C.F.	12	1
Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	LINARES DEPORTIVO	1	7
Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	2	7
Trofeo Copa Subdelegado del Gobierno (Jaén)	Temporada 2024-2025	RECREATIVO DE BAILEN C.F.	3	2
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. ATLETICO MENGIBAR	1	68
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	VILLARGORDO C.F.	2	63
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	CLUB DEPORTIVO JAÉN F.C. "B"	3	55
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	U.D. GUARROMAN	4	48
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	ATLETICO DE PORCUNA C.F.	5	46
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	ASOC.DVA. LOPERA	6	44
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. LINARES CLUB DE FÚTBOL "B"	7	43
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	8	43
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. UTICA	9	34
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	INTER DE JAEN C.F. "B"	10	24
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	RECREATIVO DE BAILEN C.F. "B"	11	20
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	URGAVONA C.F.	12	16
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	C.D. TUCCITANA "B"	13	11
3ª Andaluza Juvenil (Jaén)	Temporada 2024-2025	CLUB DEPORTIVO LONCHU "A"	14	-2
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. UBEDA VIVA	1	38
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	ATLETICO JIENNENSE F.C.F.	2	32
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. ALCALA ENJOY DESGUACES AUTOCOCHE	3	27
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	LINARES DEPORTIVO	4	22
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	REAL JAEN C.F., S.A.D. "B"	5	18
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	MARTOS C.D.	6	13
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	7	13
Liga Fomento Femenino Sénior Fútbol 7 (Jaén)	Temporada 2024-2025	TORREPEROGIL C.D.	8	0
2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	3	47
\.


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


--
-- Data for Name: predice; Type: TABLE DATA; Schema: public; Owner: admin_bd
--

COPY public.predice (dni, nombre_competicion, temporada_competicion, local, visitante, pagado, resultado_local, resultado_visitante) FROM stdin;
26520115B	2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	LINARES DEPORTIVO B	f	3	0
26520115B	2ª Andaluza Sénior (Jaén)	Temporada 2024-2025	C.D. CAMPILLO DEL RÍO C.F.	LINARES DEPORTIVO B	t	2	0
\.



--
-- Name: abono_id_abono_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_bd
--

SELECT pg_catalog.setval('public.abono_id_abono_seq', 1, true);


--
-- Name: cesion_abono_id_cesion_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_bd
--

SELECT pg_catalog.setval('public.cesion_abono_id_cesion_seq', 3, true);


--
-- Name: equipo_id_equipo_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_bd
--

SELECT pg_catalog.setval('public.equipo_id_equipo_seq', 3, true);


--
-- Name: jugador_id_jugador_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_bd
--

SELECT pg_catalog.setval('public.jugador_id_jugador_seq', 66, true);


--
-- Name: noticia_id_noticia_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_bd
--

SELECT pg_catalog.setval('public.noticia_id_noticia_seq', 4, true);


--
-- Name: patrocinador_id_patrocinador_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_bd
--

SELECT pg_catalog.setval('public.patrocinador_id_patrocinador_seq', 31, true);


--
-- Name: pedido_id_pedido_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_bd
--

SELECT pg_catalog.setval('public.pedido_id_pedido_seq', 34, true);


--
-- Name: pedido_producto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pedido_producto_id_seq', 48, true);


--
-- Name: post_foro_id_post_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_bd
--

SELECT pg_catalog.setval('public.post_foro_id_post_seq', 1, false);


--
-- Name: producto_id_producto_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_bd
--

SELECT pg_catalog.setval('public.producto_id_producto_seq', 4, true);


--
-- PostgreSQL database dump complete
--

