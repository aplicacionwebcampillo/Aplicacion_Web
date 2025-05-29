-
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
-- Name: abono id_abono; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.abono ALTER COLUMN id_abono SET DEFAULT nextval('public.abono_id_abono_seq'::regclass);


--
-- Name: cesion_abono id_cesion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono ALTER COLUMN id_cesion SET DEFAULT nextval('public.cesion_abono_id_cesion_seq'::regclass);


--
-- Name: equipo id_equipo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.equipo ALTER COLUMN id_equipo SET DEFAULT nextval('public.equipo_id_equipo_seq'::regclass);


--
-- Name: jugador id_jugador; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jugador ALTER COLUMN id_jugador SET DEFAULT nextval('public.jugador_id_jugador_seq'::regclass);


--
-- Name: noticia id_noticia; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.noticia ALTER COLUMN id_noticia SET DEFAULT nextval('public.noticia_id_noticia_seq'::regclass);


--
-- Name: patrocinador id_patrocinador; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patrocinador ALTER COLUMN id_patrocinador SET DEFAULT nextval('public.patrocinador_id_patrocinador_seq'::regclass);


--
-- Name: pedido id_pedido; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido ALTER COLUMN id_pedido SET DEFAULT nextval('public.pedido_id_pedido_seq'::regclass);


--
-- Name: pedido_producto id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_producto ALTER COLUMN id SET DEFAULT nextval('public.pedido_producto_id_seq'::regclass);


--
-- Name: post_foro id_post; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_foro ALTER COLUMN id_post SET DEFAULT nextval('public.post_foro_id_post_seq'::regclass);


--
-- Name: producto id_producto; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto ALTER COLUMN id_producto SET DEFAULT nextval('public.producto_id_producto_seq'::regclass);


--
-- Name: abono abono_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.abono
    ADD CONSTRAINT abono_pkey PRIMARY KEY (id_abono);


--
-- Name: administrador administrador_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_pkey PRIMARY KEY (dni);


--
-- Name: cesion_abono cesion_abono_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono
    ADD CONSTRAINT cesion_abono_pkey PRIMARY KEY (id_cesion);


--
-- Name: clasificacion clasificacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clasificacion
    ADD CONSTRAINT clasificacion_pkey PRIMARY KEY (nombre_competicion, temporada_competicion, equipo);


--
-- Name: competicion competicion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competicion
    ADD CONSTRAINT competicion_pkey PRIMARY KEY (nombre, temporada);


--
-- Name: compra compra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_pkey PRIMARY KEY (dni, id_pedido);


--
-- Name: equipo equipo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.equipo
    ADD CONSTRAINT equipo_pkey PRIMARY KEY (id_equipo);


--
-- Name: jugador jugador_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT jugador_pkey PRIMARY KEY (id_jugador, id_equipo);


--
-- Name: noticia noticia_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.noticia
    ADD CONSTRAINT noticia_pkey PRIMARY KEY (id_noticia);


--
-- Name: noticia noticia_titular_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.noticia
    ADD CONSTRAINT noticia_titular_key UNIQUE (titular);


--
-- Name: partido partido_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_pkey PRIMARY KEY (nombre_competicion, temporada_competicion, local, visitante);


--
-- Name: patrocinador patrocinador_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patrocinador
    ADD CONSTRAINT patrocinador_pkey PRIMARY KEY (id_patrocinador);


--
-- Name: pedido pedido_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido
    ADD CONSTRAINT pedido_pkey PRIMARY KEY (id_pedido);


--
-- Name: pedido_producto pedido_producto_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_producto
    ADD CONSTRAINT pedido_producto_pkey PRIMARY KEY (id);


--
-- Name: post_foro post_foro_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_foro
    ADD CONSTRAINT post_foro_pkey PRIMARY KEY (id_post);


--
-- Name: predice predice_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.predice
    ADD CONSTRAINT predice_pkey PRIMARY KEY (dni, nombre_competicion, temporada_competicion, local, visitante, resultado_local, resultado_visitante);


--
-- Name: producto producto_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_nombre_key UNIQUE (nombre);


--
-- Name: producto producto_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_pkey PRIMARY KEY (id_producto);


--
-- Name: socio_abono socio_abono_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio_abono
    ADD CONSTRAINT socio_abono_pkey PRIMARY KEY (dni, id_abono);


--
-- Name: socio socio_num_socio_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio
    ADD CONSTRAINT socio_num_socio_key UNIQUE (num_socio);


--
-- Name: socio socio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio
    ADD CONSTRAINT socio_pkey PRIMARY KEY (dni);


--
-- Name: usuario usuario_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_email_key UNIQUE (email);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (dni);


--
-- Name: idx_jugador_equipo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_jugador_equipo ON public.jugador USING btree (nombre);


--
-- Name: idx_noticia_categoria; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_noticia_categoria ON public.noticia USING btree (categoria);


--
-- Name: idx_partido_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_partido_fecha ON public.partido USING btree (dia);


--
-- Name: idx_producto_categoria; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_producto_categoria ON public.producto USING btree (nombre);


--
-- Name: idx_socio_num_socio; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_socio_num_socio ON public.socio USING btree (dni);


--
-- Name: idx_usuario_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_usuario_email ON public.usuario USING btree (dni);


--
-- Name: producto trigger_evitar_stock_negativo; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_evitar_stock_negativo BEFORE UPDATE ON public.producto FOR EACH ROW EXECUTE FUNCTION public.evitar_stock_negativo();


--
-- Name: noticia trigger_validar_categoria_noticia; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_categoria_noticia BEFORE INSERT OR UPDATE OF categoria ON public.noticia FOR EACH ROW EXECUTE FUNCTION public.validar_categoria_noticia();


--
-- Name: cesion_abono trigger_validar_cesion_abono; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_cesion_abono BEFORE INSERT ON public.cesion_abono FOR EACH ROW EXECUTE FUNCTION public.validar_cesion_abono();


--
-- Name: socio_abono trigger_validar_compra_abono; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_compra_abono BEFORE INSERT ON public.socio_abono FOR EACH ROW EXECUTE FUNCTION public.validar_compra_abono();


--
-- Name: usuario trigger_validar_contrasena_usuario; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_contrasena_usuario BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_contrasena_usuario();


--
-- Name: usuario trigger_validar_dni; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_dni BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_dni_usuario();


--
-- Name: jugador trigger_validar_dorsal_unico; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_dorsal_unico BEFORE INSERT OR UPDATE ON public.jugador FOR EACH ROW EXECUTE FUNCTION public.validar_dorsal_unico();


--
-- Name: usuario trigger_validar_edad; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_edad BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_edad_usuario();


--
-- Name: post_foro trigger_validar_edicion_publicacion; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_edicion_publicacion BEFORE UPDATE ON public.post_foro FOR EACH ROW EXECUTE FUNCTION public.validar_edicion_publicacion();


--
-- Name: competicion trigger_validar_eliminacion_competicion; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_eliminacion_competicion BEFORE DELETE ON public.competicion FOR EACH ROW EXECUTE FUNCTION public.validar_eliminacion_competicion();


--
-- Name: jugador trigger_validar_eliminacion_jugador; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_eliminacion_jugador BEFORE DELETE ON public.jugador FOR EACH ROW EXECUTE FUNCTION public.validar_eliminacion_jugador();


--
-- Name: producto trigger_validar_eliminacion_producto; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_eliminacion_producto BEFORE DELETE ON public.producto FOR EACH ROW EXECUTE FUNCTION public.validar_eliminacion_producto();


--
-- Name: post_foro trigger_validar_eliminacion_publicacion_simple; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_eliminacion_publicacion_simple BEFORE DELETE ON public.post_foro FOR EACH ROW EXECUTE FUNCTION public.validar_eliminacion_publicacion_simple('current_user_dni');


--
-- Name: usuario trigger_validar_email_usuario; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_email_usuario BEFORE INSERT OR UPDATE ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_email_usuario();


--
-- Name: competicion trigger_validar_modificacion_competicion; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_modificacion_competicion BEFORE UPDATE ON public.competicion FOR EACH ROW EXECUTE FUNCTION public.validar_modificacion_competicion();


--
-- Name: jugador trigger_validar_modificacion_jugador; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_modificacion_jugador BEFORE UPDATE ON public.jugador FOR EACH ROW EXECUTE FUNCTION public.validar_modificacion_jugador();


--
-- Name: producto trigger_validar_modificacion_producto; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_modificacion_producto BEFORE UPDATE ON public.producto FOR EACH ROW EXECUTE FUNCTION public.validar_modificacion_producto();


--
-- Name: noticia trigger_validar_noticia; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_noticia BEFORE INSERT OR UPDATE ON public.noticia FOR EACH ROW EXECUTE FUNCTION public.validar_noticia();


--
-- Name: post_foro trigger_validar_publicacion_foro; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_publicacion_foro BEFORE INSERT ON public.post_foro FOR EACH ROW EXECUTE FUNCTION public.validar_publicacion_foro();


--
-- Name: socio_abono trigger_validar_renovacion_abono; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_renovacion_abono BEFORE UPDATE ON public.socio_abono FOR EACH ROW EXECUTE FUNCTION public.validar_renovacion_abono();


--
-- Name: administrador trigger_validar_rol_administrador; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_rol_administrador BEFORE INSERT OR UPDATE OF cargo ON public.administrador FOR EACH ROW EXECUTE FUNCTION public.validar_rol_administrador();


--
-- Name: usuario trigger_validar_telefono_usuario; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_validar_telefono_usuario BEFORE INSERT OR UPDATE OF telefono ON public.usuario FOR EACH ROW EXECUTE FUNCTION public.validar_telefono_usuario();


--
-- Name: administrador administrador_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_dni_fkey FOREIGN KEY (dni) REFERENCES public.usuario(dni);


--
-- Name: cesion_abono cesion_abono_dni_beneficiario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono
    ADD CONSTRAINT cesion_abono_dni_beneficiario_fkey FOREIGN KEY (dni_beneficiario) REFERENCES public.usuario(dni);


--
-- Name: cesion_abono cesion_abono_dni_cedente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono
    ADD CONSTRAINT cesion_abono_dni_cedente_fkey FOREIGN KEY (dni_cedente) REFERENCES public.socio(dni);


--
-- Name: cesion_abono cesion_abono_id_abono_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cesion_abono
    ADD CONSTRAINT cesion_abono_id_abono_fkey FOREIGN KEY (id_abono) REFERENCES public.abono(id_abono);


--
-- Name: clasificacion clasificacion_nombre_competicion_temporada_competicion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clasificacion
    ADD CONSTRAINT clasificacion_nombre_competicion_temporada_competicion_fkey FOREIGN KEY (nombre_competicion, temporada_competicion) REFERENCES public.competicion(nombre, temporada) ON DELETE CASCADE;


--
-- Name: competicion competicion_id_equipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competicion
    ADD CONSTRAINT competicion_id_equipo_fkey FOREIGN KEY (id_equipo) REFERENCES public.equipo(id_equipo) ON DELETE CASCADE;


--
-- Name: compra compra_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_dni_fkey FOREIGN KEY (dni) REFERENCES public.usuario(dni);


--
-- Name: compra compra_id_pedido_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_id_pedido_fkey FOREIGN KEY (id_pedido) REFERENCES public.pedido(id_pedido) ON DELETE RESTRICT;


--
-- Name: noticia fk_noticia_admin; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.noticia
    ADD CONSTRAINT fk_noticia_admin FOREIGN KEY (dni_administrador) REFERENCES public.administrador(dni);


--
-- Name: patrocinador fk_patrocinador_admin; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patrocinador
    ADD CONSTRAINT fk_patrocinador_admin FOREIGN KEY (dni_administrador) REFERENCES public.administrador(dni);


--
-- Name: post_foro fk_post_foro_usuario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.post_foro
    ADD CONSTRAINT fk_post_foro_usuario FOREIGN KEY (dni_usuario) REFERENCES public.usuario(dni) ON DELETE CASCADE;


--
-- Name: jugador jugador_id_equipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT jugador_id_equipo_fkey FOREIGN KEY (id_equipo) REFERENCES public.equipo(id_equipo) ON DELETE SET NULL;


--
-- Name: partido partido_nombre_competicion_temporada_competicion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partido
    ADD CONSTRAINT partido_nombre_competicion_temporada_competicion_fkey FOREIGN KEY (nombre_competicion, temporada_competicion) REFERENCES public.competicion(nombre, temporada) ON DELETE CASCADE;


--
-- Name: pedido_producto pedido_producto_pedido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_producto
    ADD CONSTRAINT pedido_producto_pedido_id_fkey FOREIGN KEY (pedido_id) REFERENCES public.pedido(id_pedido) ON DELETE CASCADE;


--
-- Name: pedido_producto pedido_producto_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pedido_producto
    ADD CONSTRAINT pedido_producto_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.producto(id_producto) ON DELETE CASCADE;


--
-- Name: predice predice_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.predice
    ADD CONSTRAINT predice_dni_fkey FOREIGN KEY (dni) REFERENCES public.socio(dni);


--
-- Name: predice predice_nombre_competicion_temporada_competicion_local_vis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.predice
    ADD CONSTRAINT predice_nombre_competicion_temporada_competicion_local_vis_fkey FOREIGN KEY (nombre_competicion, temporada_competicion, local, visitante) REFERENCES public.partido(nombre_competicion, temporada_competicion, local, visitante) ON DELETE CASCADE;


--
-- Name: socio_abono socio_abono_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio_abono
    ADD CONSTRAINT socio_abono_dni_fkey FOREIGN KEY (dni) REFERENCES public.socio(dni);


--
-- Name: socio_abono socio_abono_id_abono_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio_abono
    ADD CONSTRAINT socio_abono_id_abono_fkey FOREIGN KEY (id_abono) REFERENCES public.abono(id_abono) ON DELETE RESTRICT;


--
-- Name: socio socio_dni_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.socio
    ADD CONSTRAINT socio_dni_fkey FOREIGN KEY (dni) REFERENCES public.usuario(dni);


--
-- Name: TABLE pedido_producto; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.pedido_producto TO admin_bd;


--
-- Name: SEQUENCE pedido_producto_id_seq; Type: ACL; Schema: public; Owner: -
--

GRANT SELECT,USAGE ON SEQUENCE public.pedido_producto_id_seq TO admin_bd;


--
-- PostgreSQL database dump complete
--

