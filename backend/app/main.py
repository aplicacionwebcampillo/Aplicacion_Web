from fastapi import FastAPI
from app.database import Base, engine

from fastapi.middleware.cors import CORSMiddleware

from app.routers.usuario import router as usuario_router
from app.routers.administrador import router as administrador_router
from app.routers.socio import router as socio_router
from app.routers.producto import router as producto_router
from app.routers.noticia import router as noticia_router
from app.routers.patrocinador import router as patrocinador_router
from app.routers.foro import router as foro_router
from app.routers.jugador import router as jugador_router
from app.routers.partido import router as partido_router
from app.routers.cesion_abono import router as cesion_abono_router
from app.routers.competicion import router as competicion_router
from app.routers.pedido import router as pedido_router
from app.routers.compra import router as compra_router
from app.routers.equipo import router as equipo_router
from app.routers.predice import router as predice_router
from app.routers.socio_abono import router as socio_abono_router
from app.routers.abono import router as abono_router
from app.routers.carrito import router as carrito_router
from app.routers.auth import router as auth_router
from app.routers.clasificacion import router as clasificacion_router


app = FastAPI(
    title="API - Campillo del Río CF",
    description="Backend para la gestión de un club de fútbol",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aplicacion-web-frontend.onrender.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar todos los routers
app.include_router(usuario_router)
app.include_router(administrador_router)
app.include_router(socio_router)
app.include_router(producto_router)
app.include_router(noticia_router)
app.include_router(patrocinador_router)
app.include_router(foro_router)
app.include_router(jugador_router)
app.include_router(partido_router)
app.include_router(cesion_abono_router)
app.include_router(competicion_router)
app.include_router(pedido_router)
app.include_router(compra_router)
app.include_router(equipo_router)
app.include_router(predice_router)
app.include_router(socio_abono_router)
app.include_router(abono_router)
app.include_router(carrito_router)
app.include_router(auth_router)
app.include_router(clasificacion_router)

