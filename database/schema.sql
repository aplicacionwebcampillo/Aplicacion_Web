-- Tabla principal de usuarios
CREATE TABLE Usuario (
    dni VARCHAR(9) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    fecha_nacimiento DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL
);

-- Tabla de socios (extiende Usuario)
CREATE TABLE Socio (
    dni VARCHAR(9) PRIMARY KEY REFERENCES Usuario(dni),
    num_socio VARCHAR(20) UNIQUE NOT NULL,
    foto_perfil VARCHAR(255),
    tipo_membresia VARCHAR(30) NOT NULL,
    estado VARCHAR(15) DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'suspendido'))
);

-- Tabla de administradores (extiende Usuario)
CREATE TABLE Administrador (
    dni VARCHAR(9) PRIMARY KEY REFERENCES Usuario(dni),
    cargo VARCHAR(50) NOT NULL,
    permisos VARCHAR(50) NOT NULL,
    foto_perfil VARCHAR(255),
    estado VARCHAR(15) DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo'))
);

-- Tabla de abonos
CREATE TABLE Abono (
    id_abono SERIAL PRIMARY KEY,
    temporada VARCHAR(20) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    CONSTRAINT fechas_validas CHECK (fecha_fin > fecha_inicio)
);

-- Tabla de posts del foro
CREATE TABLE Post_Foro (
    id_post SERIAL PRIMARY KEY,
    contenido TEXT NOT NULL,
    moderado BOOLEAN DEFAULT FALSE,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('discusion', 'encuesta', 'votacion')),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de pedidos
CREATE TABLE Pedido (
    id_pedido SERIAL PRIMARY KEY,
    descuento DECIMAL(10,2) DEFAULT 0.00,
    precio_total DECIMAL(10,2) NOT NULL,
    cantidad INTEGER
);

-- Tabla de productos de la tienda
CREATE TABLE Producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    imagen VARCHAR(255) NOT NULL
);

-- Tabla de noticias
CREATE TABLE Noticia (
    id_noticia SERIAL PRIMARY KEY,
    titular VARCHAR(200) NOT NULL UNIQUE,
    imagen VARCHAR(255),
    contenido TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL
);

-- Tabla de patrocinadores
CREATE TABLE Patrocinador (
    id_patrocinador SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(15),
    logo VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE
);

-- Tabla de equipos
CREATE TABLE Equipo (
    id_equipo SERIAL PRIMARY KEY,
    categoria VARCHAR(50) NOT NULL,
    num_jugadores INTEGER NOT NULL DEFAULT 0
);

-- Tabla de jugadores
CREATE TABLE Jugador (
    id_jugador SERIAL,
    id_equipo INTEGER REFERENCES Equipo(id_equipo) ON DELETE SET NULL,
    nombre VARCHAR(100) NOT NULL,
    posicion VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    foto VARCHAR(255),
    biografia TEXT,
    PRIMARY KEY (id_jugador, id_equipo)
);

-- Tabla de competiciones
CREATE TABLE Competicion (
    nombre VARCHAR(100) NOT NULL,
    temporada VARCHAR(20) NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'en_progreso', 'finalizada')),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    PRIMARY KEY (nombre, temporada)
);

-- Tabla de partidos
CREATE TABLE Partido (
    nombre_competicion VARCHAR(100) NOT NULL,
    temporada_competicion VARCHAR(20) NOT NULL,
    local VARCHAR(100) NOT NULL,
    visitante VARCHAR(100) NOT NULL,
    dia DATE NOT NULL,
    hora TIME NOT NULL,
    resultado VARCHAR(20),
    estadio VARCHAR(100),
    FOREIGN KEY (nombre_competicion, temporada_competicion) REFERENCES Competicion(nombre, temporada) ON DELETE CASCADE,
    PRIMARY KEY (nombre_competicion, temporada_competicion, local, visitante)
);

-- Tabla de relación Tiene Socio-Abono
CREATE TABLE Socio_Abono (
    dni VARCHAR(9) REFERENCES Socio(dni),
    id_abono INTEGER REFERENCES Abono(id_abono) ON DELETE RESTRICT,
    fecha_compra DATE NOT NULL DEFAULT CURRENT_DATE,
    pagado BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (dni, id_abono)
);

-- Tabla de relación Compra Usuario-Pedido
CREATE TABLE Compra (
    dni VARCHAR(9) REFERENCES Usuario(dni),
    id_pedido INTEGER REFERENCES Pedido(id_pedido) ON DELETE RESTRICT,
    fecha_compra DATE NOT NULL DEFAULT CURRENT_DATE,
    pagado BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (dni, id_pedido)
);

-- Tabla de predicciones de resultados Socio-Partido
CREATE TABLE Predice (
    dni VARCHAR(9) REFERENCES Socio(dni),
    nombre_competicion VARCHAR(100) NOT NULL,
    temporada_competicion VARCHAR(20) NOT NULL,
    local VARCHAR(100) NOT NULL,
    visitante VARCHAR(100) NOT NULL,
    resultado VARCHAR(20) NOT NULL,
    pagado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (nombre_competicion, temporada_competicion, local, visitante) 
        REFERENCES Partido(nombre_competicion, temporada_competicion, local, visitante) ON DELETE CASCADE,
    PRIMARY KEY (dni, nombre_competicion, temporada_competicion, local, visitante)
);

CREATE TABLE clasificacion (
     nombre_competicion VARCHAR(100) NOT NULL,
     temporada_competicion VARCHAR(20) NOT NULL,
     equipo VARCHAR(100) NOT NULL,
     posicion INTEGER NOT NULL,
     puntos INTEGER NOT NULL,
     PRIMARY KEY (nombre_competicion, temporada_competicion, equipo),
     FOREIGN KEY (nombre_competicion, temporada_competicion)
         REFERENCES competicion(nombre, temporada)
         ON DELETE CASCADE
);





-- Índices para búsquedas frecuentes
CREATE INDEX idx_usuario_email ON Usuario(dni);
CREATE INDEX idx_socio_num_socio ON Socio(dni);
CREATE INDEX idx_producto_categoria ON Producto(nombre);
CREATE INDEX idx_noticia_categoria ON Noticia(categoria);
CREATE INDEX idx_partido_fecha ON Partido(dia);
CREATE INDEX idx_jugador_equipo ON Jugador(nombre);






