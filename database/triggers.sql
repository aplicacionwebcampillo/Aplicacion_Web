CREATE OR REPLACE FUNCTION validar_rol_administrador()
RETURNS TRIGGER AS $$
BEGIN
    -- Lista de roles predefinidos válidos
    IF NEW.cargo NOT IN ('Administrador General', 'Administrador de Contenidos', 'Administrador de Sistemas') THEN
        RAISE EXCEPTION 'El rol "%" no es válido. Roles permitidos: "Administrador General", "Administrador de Contenidos", "Administrador de Sistemas"', NEW.cargo;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_rol_administrador
BEFORE INSERT OR UPDATE OF cargo ON Administrador
FOR EACH ROW EXECUTE FUNCTION validar_rol_administrador();

---------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validar_email_usuario()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email !~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$' THEN
        RAISE EXCEPTION 'El email no tiene un formato válido';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_email_usuario
BEFORE INSERT OR UPDATE ON Usuario
FOR EACH ROW EXECUTE FUNCTION validar_email_usuario();

CREATE OR REPLACE FUNCTION validar_contrasena_usuario()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.contrasena !~ '^(?=.*[A-Za-z])(?=.*\d).{8,}$' THEN
        RAISE EXCEPTION 'La contraseña debe ser alfanumérica y tener más de 8 caracteres';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_contrasena_usuario
BEFORE INSERT OR UPDATE ON Usuario
FOR EACH ROW EXECUTE FUNCTION validar_contrasena_usuario();

CREATE OR REPLACE FUNCTION validar_dni_usuario()
RETURNS TRIGGER AS $$
DECLARE
    letras_dni CHAR(23) := 'TRWAGMYFPDXBNJZSQVHLCKE';
    num_dni INTEGER;
    letra_calculada CHAR;
BEGIN
    IF NEW.dni !~ '^\d{8}[A-Za-z]$' THEN
        RAISE EXCEPTION 'El DNI debe tener 8 números y una letra';
    END IF;
    
    num_dni := SUBSTRING(NEW.dni FROM 1 FOR 8)::INTEGER;
    letra_calculada := UPPER(SUBSTRING(letras_dni FROM (num_dni % 23)+1 FOR 1));
    
    IF UPPER(SUBSTRING(NEW.dni FROM 9 FOR 1)) != letra_calculada THEN
        RAISE EXCEPTION 'La letra del DNI no es válida';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_dni
BEFORE INSERT OR UPDATE ON Usuario
FOR EACH ROW EXECUTE FUNCTION validar_dni_usuario();


CREATE OR REPLACE FUNCTION validar_telefono_usuario()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar que el teléfono tenga valor cuando se proporciona
    IF NEW.telefono IS NOT NULL THEN
        -- Validar formato básico de teléfono (9 dígitos para España)
        IF NEW.telefono !~ '^[+]?[0-9]{9,15}$' THEN
            RAISE EXCEPTION 'El teléfono "%" no tiene un formato válido.', NEW.telefono;
        END IF;
        
        -- Validar que el teléfono no esté duplicado (opcional, según requisitos)
        IF EXISTS (SELECT 1 FROM Usuario WHERE telefono = NEW.telefono AND dni != NEW.dni) THEN
            RAISE EXCEPTION 'El teléfono "%" ya está registrado en el sistema', NEW.telefono;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_telefono_usuario
BEFORE INSERT OR UPDATE OF telefono ON Usuario
FOR EACH ROW EXECUTE FUNCTION validar_telefono_usuario();

CREATE OR REPLACE FUNCTION validar_edad_usuario()
RETURNS TRIGGER AS $$
BEGIN
    IF AGE(NEW.fecha_nacimiento) < INTERVAL '12 years' THEN
        RAISE EXCEPTION 'El usuario debe tener al menos 12 años';
    END IF;
    IF AGE(NEW.fecha_nacimiento) > INTERVAL '110 years' THEN
        RAISE EXCEPTION 'La edad no puede superar los 110 años';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_edad
BEFORE INSERT OR UPDATE ON Usuario
FOR EACH ROW EXECUTE FUNCTION validar_edad_usuario();

-------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validar_compra_abono()
RETURNS TRIGGER AS $$
DECLARE
    abono_activo BOOLEAN;
BEGIN
    -- Verificar si el usuario ya tiene un abono activo
    SELECT EXISTS (
        SELECT 1 FROM Socio_Abono sa
        JOIN Abono a ON sa.id_abono = a.id_abono
        WHERE sa.dni = NEW.dni 
        AND a.fecha_fin >= CURRENT_DATE
        AND sa.pagado = TRUE
    ) INTO abono_activo;
    
    IF abono_activo THEN
        RAISE EXCEPTION 'El usuario ya tiene un abono activo';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_compra_abono
BEFORE INSERT ON Socio_Abono
FOR EACH ROW EXECUTE FUNCTION validar_compra_abono();

CREATE OR REPLACE FUNCTION validar_renovacion_abono()
RETURNS TRIGGER AS $$
DECLARE
    dias_restantes INTEGER;
BEGIN
    -- Solo permitir renovación si el abono está próximo a expirar (últimos 30 días)
    SELECT (a.fecha_fin - CURRENT_DATE) 
    INTO dias_restantes
    FROM Abono a
    WHERE a.id_abono = NEW.id_abono;
    
    IF dias_restantes > 30 THEN
        RAISE EXCEPTION 'Solo se puede renovar el abono en los últimos 30 días antes de su expiración';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_renovacion_abono
BEFORE UPDATE ON Socio_Abono
FOR EACH ROW EXECUTE FUNCTION validar_renovacion_abono();

CREATE OR REPLACE FUNCTION validar_cesion_abono()
RETURNS TRIGGER AS $$
DECLARE
    abono_activo_beneficiario BOOLEAN;
    es_socio_beneficiario BOOLEAN;
BEGIN
    -- Verificar que el beneficiario esté registrado
    SELECT EXISTS (
        SELECT 1 FROM Usuario
        WHERE dni = NEW.dni_beneficiario
    ) INTO es_socio_beneficiario;
    
    IF NOT es_socio_beneficiario THEN
        RAISE EXCEPTION 'El beneficiario con DNI % no está registrado', NEW.dni_beneficiario;
    END IF;
    
    -- Verificar que el beneficiario no tenga un abono activo
    SELECT EXISTS (
        SELECT 1 FROM Socio_Abono sa
        JOIN Abono a ON sa.id_abono = a.id_abono
        WHERE sa.dni = NEW.dni_beneficiario
        AND a.fecha_fin >= CURRENT_DATE
        AND sa.pagado = TRUE
    ) INTO abono_activo_beneficiario;
    
    IF abono_activo_beneficiario THEN
        RAISE EXCEPTION 'El beneficiario con DNI % ya tiene un abono activo', NEW.dni_beneficiario;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Necesitarás una tabla para registrar las cesiones temporales
CREATE TABLE IF NOT EXISTS Cesion_Abono (
    id_cesion SERIAL PRIMARY KEY,
    dni_cedente VARCHAR(9) NOT NULL REFERENCES Socio(dni),
    dni_beneficiario VARCHAR(9) NOT NULL REFERENCES Socio(dni),
    id_abono INTEGER NOT NULL REFERENCES Abono(id_abono),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    fecha_cesion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fechas_cesion_validas CHECK (fecha_fin > fecha_inicio),
    CONSTRAINT cedente_beneficiario_diferentes CHECK (dni_cedente <> dni_beneficiario)
);

CREATE TRIGGER trigger_validar_cesion_abono
BEFORE INSERT ON Cesion_Abono
FOR EACH ROW EXECUTE FUNCTION validar_cesion_abono();

------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validar_modificacion_producto()
RETURNS TRIGGER AS $$
DECLARE
    en_compra BOOLEAN;
BEGIN
    -- Verificar si el producto está en una compra en proceso
    SELECT EXISTS (
        SELECT 1 FROM Pedido p
        JOIN Compra c ON p.id_pedido = c.id_pedido
        WHERE p.id_producto = NEW.id_producto
        AND c.pagado = FALSE
    ) INTO en_compra;
    
    IF en_compra THEN
        RAISE EXCEPTION 'No se puede modificar un producto asociado a una compra en proceso';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_modificacion_producto
BEFORE UPDATE ON Producto
FOR EACH ROW EXECUTE FUNCTION validar_modificacion_producto();

CREATE OR REPLACE FUNCTION validar_eliminacion_producto()
RETURNS TRIGGER AS $$
DECLARE
    tiene_stock BOOLEAN;
    en_compra BOOLEAN;
BEGIN
    -- Verificar si el producto tiene stock
    IF OLD.stock > 0 THEN
        RAISE EXCEPTION 'No se puede eliminar un producto con stock disponible';
    END IF;
    
    -- Verificar si el producto está en una compra pendiente
    SELECT EXISTS (
        SELECT 1 FROM Pedido p
        JOIN Compra c ON p.id_pedido = c.id_pedido
        WHERE p.id_producto = OLD.id_producto
        AND c.pagado = FALSE
    ) INTO en_compra;
    
    IF en_compra THEN
        RAISE EXCEPTION 'No se puede eliminar un producto asociado a una compra pendiente';
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_eliminacion_producto
BEFORE DELETE ON Producto
FOR EACH ROW EXECUTE FUNCTION validar_eliminacion_producto();

------------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validar_noticia()
RETURNS TRIGGER AS $$
BEGIN
    -- Validar título
    IF NEW.titular IS NULL OR LENGTH(TRIM(NEW.titular)) = 0 THEN
        RAISE EXCEPTION 'El título de la noticia no puede estar vacío';
    END IF;
    
    IF LENGTH(NEW.titular) > 100 THEN
        RAISE EXCEPTION 'El título no puede superar los 100 caracteres';
    END IF;
    
    -- Validar contenido
    IF NEW.contenido IS NULL OR LENGTH(TRIM(NEW.contenido)) < 50 THEN
        RAISE EXCEPTION 'El contenido debe tener al menos 50 caracteres';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_noticia
BEFORE INSERT OR UPDATE ON Noticia
FOR EACH ROW EXECUTE FUNCTION validar_noticia();

CREATE OR REPLACE FUNCTION validar_categoria_noticia()
RETURNS TRIGGER AS $$
BEGIN
    -- Lista de categorías predefinidas válidas
    IF NEW.categoria NOT IN (
        'Senior Masculino',
        'Senior Femenino',  
        'Cantera', 
        'Noticias del Club',
        'Comunicados Oficiales',
        'Actividades Sociales'
    ) THEN
        RAISE EXCEPTION 'La categoría "%" no es válida. Categorías permitidas: "Senior Masculino", "Senior Masculino", "Cantera", "Noticias del Club", "Comunicados Oficiales", "Actividades Sociales"', 
        NEW.categoria;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_categoria_noticia
BEFORE INSERT OR UPDATE OF categoria ON Noticia
FOR EACH ROW EXECUTE FUNCTION validar_categoria_noticia();

----------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validar_modificacion_competicion()
RETURNS TRIGGER AS $$
BEGIN
    -- No se puede modificar si ya ha comenzado
    IF OLD.estado = 'en_progreso' OR OLD.estado = 'finalizada' THEN
        RAISE EXCEPTION 'No se puede modificar una competición que ya ha comenzado';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_modificacion_competicion
BEFORE UPDATE ON Competicion
FOR EACH ROW EXECUTE FUNCTION validar_modificacion_competicion();

CREATE OR REPLACE FUNCTION validar_eliminacion_competicion()
RETURNS TRIGGER AS $$
DECLARE
    tiene_partidos BOOLEAN;
BEGIN
    -- Verificar si tiene partidos asociados
    SELECT EXISTS (
        SELECT 1 FROM Partido
        WHERE nombre_competicion = OLD.nombre
        AND temporada_competicion = OLD.temporada
    ) INTO tiene_partidos;
    
    IF OLD.estado != 'pendiente' OR tiene_partidos THEN
        RAISE EXCEPTION 'No se puede eliminar una competición que ya ha comenzado o tiene partidos asociados';
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_eliminacion_competicion
BEFORE DELETE ON Competicion
FOR EACH ROW EXECUTE FUNCTION validar_eliminacion_competicion();

----------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validar_modificacion_jugador()
RETURNS TRIGGER AS $$
DECLARE
    en_partido BOOLEAN;
BEGIN
    -- Verificar si está en un partido activo
    SELECT EXISTS (
        SELECT 1 FROM Partido p
        JOIN Jugador j ON (p.local = j.id_equipo OR p.visitante = j.id_equipo)
        WHERE j.id_jugador = NEW.id_jugador
        AND p.dia = CURRENT_DATE
    ) INTO en_partido;
    
    IF en_partido THEN
        RAISE EXCEPTION 'No se puede modificar un jugador que está participando en un partido activo';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_modificacion_jugador
BEFORE UPDATE ON Jugador
FOR EACH ROW EXECUTE FUNCTION validar_modificacion_jugador();

CREATE OR REPLACE FUNCTION validar_eliminacion_jugador()
RETURNS TRIGGER AS $$
DECLARE
    en_competicion BOOLEAN;
BEGIN
    -- Verificar si está asociado a partidos o competiciones
    SELECT EXISTS (
        SELECT 1 FROM Partido p
        JOIN Jugador j ON (p.local = j.id_equipo OR p.visitante = j.id_equipo)
        WHERE j.id_jugador = OLD.id_jugador
    ) INTO en_competicion;
    
    IF en_competicion THEN
        RAISE EXCEPTION 'No se puede eliminar un jugador asociado a partidos o competiciones';
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_eliminacion_jugador
BEFORE DELETE ON Jugador
FOR EACH ROW EXECUTE FUNCTION validar_eliminacion_jugador();

----------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION validar_publicacion_foro()
RETURNS TRIGGER AS $$
DECLARE
    publicaciones_pendientes INTEGER;
BEGIN
    -- Verificar si el usuario tiene publicaciones pendientes de moderación
    SELECT COUNT(*) 
    INTO publicaciones_pendientes
    FROM Post_Foro
    WHERE dni_autor = NEW.dni_autor
    AND moderado = FALSE;
    
    IF publicaciones_pendientes > 0 THEN
        RAISE EXCEPTION 'El usuario tiene publicaciones pendientes de moderación';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_publicacion_foro
BEFORE INSERT ON Post_Foro
FOR EACH ROW EXECUTE FUNCTION validar_publicacion_foro();

CREATE OR REPLACE FUNCTION validar_edicion_publicacion()
RETURNS TRIGGER AS $$
BEGIN
    -- Solo el autor puede editar
    IF OLD.dni_autor != NEW.dni_autor THEN
        RAISE EXCEPTION 'Solo el autor puede editar la publicación';
    END IF;
    
    -- No se puede editar si ha sido reportada
    IF OLD.reportado = TRUE THEN
        RAISE EXCEPTION 'No se puede editar una publicación reportada';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_edicion_publicacion
BEFORE UPDATE ON Post_Foro
FOR EACH ROW EXECUTE FUNCTION validar_edicion_publicacion();

CREATE OR REPLACE FUNCTION validar_eliminacion_publicacion_simple()
RETURNS TRIGGER AS $$
DECLARE
    es_autor BOOLEAN;
    es_administrador BOOLEAN;
BEGIN
    -- Verificar si el operador es el autor (asumiendo que pasas el DNI como parámetro)
    es_autor := (OLD.dni_autor = TG_ARGV[0]);
    
    -- Verificar si el operador es administrador
    SELECT EXISTS (
        SELECT 1 FROM Administrador 
        WHERE dni = TG_ARGV[0]
    ) INTO es_administrador;
    
    -- Solo permitir eliminación por autor (si no está reportada) o administrador
    IF NOT ((es_autor AND NOT OLD.reportado) OR es_administrador) THEN
        RAISE EXCEPTION 'Solo el autor (si no está reportada) o un administrador pueden eliminar publicaciones';
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_eliminacion_publicacion_simple
BEFORE DELETE ON Post_Foro
FOR EACH ROW  EXECUTE FUNCTION validar_eliminacion_publicacion_simple(current_user_dni); 
-- Debes pasar el DNI del usuario actual

------------------------------------------------------------------------------------------------

