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
