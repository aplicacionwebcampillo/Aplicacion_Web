CREATE OR REPLACE FUNCTION registrar_usuario(
    p_dni VARCHAR(9),
    p_nombre VARCHAR(50),
    p_apellidos VARCHAR(100),
    p_telefono VARCHAR(15),
    p_fecha_nacimiento DATE,
    p_email VARCHAR(100),
    p_contrasena VARCHAR(255)
RETURNS VOID AS $$
BEGIN
    -- Insertar en tabla Usuario
    INSERT INTO Usuario (dni, nombre, apellidos, telefono, fecha_nacimiento, email, contraseña)
    VALUES (p_dni, p_nombre, p_apellidos, p_telefono, p_fecha_nacimiento, p_email, p_contrasena);
    
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION registrar_administrador(
    p_dni VARCHAR(9),
    p_nombre VARCHAR(50),
    p_apellidos VARCHAR(100),
    p_telefono VARCHAR(15),
    p_fecha_nacimiento DATE,
    p_email VARCHAR(100),
    p_contrasena VARCHAR(255),
    p_cargo VARCHAR(50),
    p_permisos VARCHAR(50))
RETURNS VOID AS $$
BEGIN
    -- Insertar en tabla Usuario
    INSERT INTO Usuario (dni, nombre, apellidos, telefono, fecha_nacimiento, email, contraseña)
    VALUES (p_dni, p_nombre, p_apellidos, p_telefono, p_fecha_nacimiento, p_email, p_contrasena);
    
    -- Insertar en tabla Administrador
    INSERT INTO Administrador (dni, cargo, permisos, estado)
    VALUES (p_dni, p_cargo, p_permisos, 'activo');
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION modificar_usuario(
    p_dni VARCHAR(9),
    p_nombre VARCHAR(50) DEFAULT NULL,
    p_apellidos VARCHAR(100) DEFAULT NULL,
    p_telefono VARCHAR(15) DEFAULT NULL,
    p_email VARCHAR(100) DEFAULT NULL,
    p_contrasena VARCHAR(255) DEFAULT NULL,
    -- Campos específicos de Socio
    p_tipo_membresia VARCHAR(30) DEFAULT NULL,
    p_foto_perfil VARCHAR(255) DEFAULT NULL,
    p_estado VARCHAR(15) DEFAULT NULL)
RETURNS VOID AS $$
DECLARE
    es_socio BOOLEAN;
BEGIN
    -- Verificar si es socio
    SELECT EXISTS (SELECT 1 FROM Socio WHERE dni = p_dni) INTO es_socio;
    
    -- Actualizar datos básicos en Usuario
    UPDATE Usuario SET
        nombre = COALESCE(p_nombre, nombre),
        apellidos = COALESCE(p_apellidos, apellidos),
        telefono = COALESCE(p_telefono, telefono),
        email = COALESCE(p_email, email),
        contraseña = CASE 
                        WHEN p_contrasena IS NOT NULL THEN crypt(p_contrasena, gen_salt('bf'))
                        ELSE contraseña 
                     END
    WHERE dni = p_dni;
    
    -- Si es socio, actualizar campos específicos
    IF es_socio THEN
        UPDATE Socio SET
            tipo_membresia = COALESCE(p_tipo_membresia, tipo_membresia),
            foto_perfil = COALESCE(p_foto_perfil, foto_perfil),
            estado = COALESCE(p_estado, estado)
        WHERE dni = p_dni;
        
        -- Validar que el estado sea uno de los permitidos
        IF p_estado IS NOT NULL AND p_estado NOT IN ('activo', 'inactivo', 'suspendido') THEN
            RAISE EXCEPTION 'El estado debe ser uno de: activo, inactivo, suspendido';
        END IF;
    END IF;
    
    -- Si se intentó modificar campos de socio pero no es socio
    IF NOT es_socio AND (p_tipo_membresia IS NOT NULL OR p_foto_perfil IS NOT NULL OR p_estado IS NOT NULL) THEN
        RAISE NOTICE 'El usuario con DNI % no es socio, se ignoraron los campos específicos de socio', p_dni;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION modificar_administrador(
    p_dni VARCHAR(9),
    p_nombre VARCHAR(50) DEFAULT NULL,
    p_apellidos VARCHAR(100) DEFAULT NULL,
    p_telefono VARCHAR(15) DEFAULT NULL,
    p_email VARCHAR(100) DEFAULT NULL,
    p_contrasena VARCHAR(255) DEFAULT NULL,
    p_cargo VARCHAR(50) DEFAULT NULL,
    p_permisos VARCHAR(50) DEFAULT NULL)
RETURNS VOID AS $$
BEGIN
    -- Actualizar datos en Usuario
    UPDATE Usuario SET
        nombre = COALESCE(p_nombre, nombre),
        apellidos = COALESCE(p_apellidos, apellidos),
        telefono = COALESCE(p_telefono, telefono),
        email = COALESCE(p_email, email),
        contraseña = CASE 
                        WHEN p_contrasena IS NOT NULL THEN crypt(p_contrasena, gen_salt('bf'))
                        ELSE contraseña 
                     END
    WHERE dni = p_dni;
    
    -- Actualizar datos específicos en Administrador
    UPDATE Administrador SET
        cargo = COALESCE(p_cargo, cargo),
        permisos = COALESCE(p_permisos, permisos)
    WHERE dni = p_dni;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_usuario(
    p_dni VARCHAR(9))
RETURNS VOID AS $$
DECLARE
    tiene_abonos_activos BOOLEAN;
BEGIN
    -- Verificar si tiene abonos activos
    SELECT EXISTS (
        SELECT 1 FROM Socio_Abono sa
        JOIN Abono a ON sa.id_abono = a.id_abono
        WHERE sa.dni = p_dni AND a.fecha_fin >= CURRENT_DATE
    ) INTO tiene_abonos_activos;
    
    IF tiene_abonos_activos THEN
        RAISE EXCEPTION 'No se puede eliminar el aficionado porque tiene abonos activos';
    END IF;
    
    -- Eliminar de Socio primero (por la FK)
    DELETE FROM Socio WHERE dni = p_dni;
    
    -- Luego eliminar de Usuario
    DELETE FROM Usuario WHERE dni = p_dni;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION eliminar_administrador(
    p_dni VARCHAR(9))
RETURNS VOID AS $$
DECLARE
    es_ultimo_admin BOOLEAN;
BEGIN
    -- Verificar si es el último administrador
    SELECT COUNT(*) = 1 INTO es_ultimo_admin
    FROM Administrador
    WHERE estado = 'activo';
    
    IF es_ultimo_admin THEN
        RAISE EXCEPTION 'No se puede eliminar el último administrador activo del sistema';
    END IF;
    
    -- Primero desactivar en Administrador
    UPDATE Administrador SET estado = 'inactivo' WHERE dni = p_dni;
    
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------------------------------------













































