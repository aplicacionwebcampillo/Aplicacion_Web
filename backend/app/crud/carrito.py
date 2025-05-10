from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.models.socio import Socio
from app.models.administrador import Administrador
from app.models.compra import Compra
from app.models.pedido_producto import pedido_producto
from app.models.pedido import Pedido
from app.schemas.carrito import AgregarProducto, AplicarDescuento
from sqlalchemy import func
from typing import List
from decimal import Decimal
from sqlalchemy import insert
import datetime

carritos = {}

def _get_carrito_usuario(user_id: int):
    if user_id not in carritos:
        carritos[user_id] = {"productos": [], "descuento": 0.0}
    return carritos[user_id]

def obtener_carrito(db: Session, user_id: int):
    carrito = _get_carrito_usuario(user_id)
    productos = []
    total = 0.0
    for item in carrito["productos"]:
        prod = db.query(Producto).filter(Producto.id_producto == item["id_producto"]).first()
        if prod:
            subtotal = prod.precio * item["cantidad"]
            productos.append({
                "id_producto": prod.id_producto,
                "nombre": prod.nombre,
                "precio": prod.precio,
                "cantidad": item["cantidad"],
                "subtotal": subtotal
            })
            total += float(subtotal)

    descuento = carrito["descuento"]
    return {
        "productos": productos,
        "precio_total": total,
        "descuento": descuento,
        "precio_final": total * (1 - descuento)
    }

def agregar_producto(db: Session, user_id: int, datos: AgregarProducto):
    carrito = _get_carrito_usuario(user_id)
    for item in carrito["productos"]:
        if item["id_producto"] == datos.id_producto:
            item["cantidad"] += datos.cantidad
            return
    carrito["productos"].append({
        "id_producto": datos.id_producto,
        "cantidad": datos.cantidad
    })

def actualizar_cantidad(db: Session, user_id: int, id_producto: int, cantidad: int):
    carrito = _get_carrito_usuario(user_id)
    for item in carrito["productos"]:
        if item["id_producto"] == id_producto:
            item["cantidad"] = cantidad
            return


def aplicar_descuento(db: Session, user_id: int, datos: AplicarDescuento):
    carrito = _get_carrito_usuario(user_id)

    usuario = db.query(Usuario).filter(Usuario.dni == user_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    socio = db.query(Socio).filter(Socio.dni == user_id).first()
    admin = db.query(Administrador).filter(Administrador.dni == user_id).first()

    if datos.codigo.upper() == "SOCIO" and socio:
        carrito["descuento"] = 0.15
    elif datos.codigo.upper() == "ADMIN" and admin:
        carrito["descuento"] = 0.25
    else:
        carrito["descuento"] = 0.0
        raise HTTPException(status_code=400, detail="Código de descuento inválido o no autorizado")

    return carrito


def confirmar_pedido(db: Session, user_id: int):
    carrito = _get_carrito_usuario(user_id)
    if not carrito["productos"]:
        return None

    total = 0.0
    for item in carrito["productos"]:
        prod = db.query(Producto).filter(Producto.id_producto == item["id_producto"]).first()
        total += float(prod.precio) * item["cantidad"]

    descuento = carrito["descuento"]
    precio_final = total * (1 - descuento)

    nuevo_pedido = Pedido(
        descuento=descuento,
        precio_total=precio_final
    )
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido) 

    nueva_compra = Compra(
        dni=user_id,
        id_pedido=nuevo_pedido.id_pedido,
        fecha_compra=datetime.date.today(),
        pagado=False
    )
    db.add(nueva_compra)
    db.commit()

    stmt = insert(pedido_producto)
    
    valores_a_insertar = [
        {
        'pedido_id': nuevo_pedido.id_pedido,
        'producto_id': item["id_producto"],
        'cantidad': item["cantidad"]
        }
        for item in carrito["productos"]
    ]
    
    db.execute(stmt, valores_a_insertar)
    db.commit()
        

    carritos[user_id] = {"productos": [], "descuento": 0.0}

    return nuevo_pedido.id_pedido

