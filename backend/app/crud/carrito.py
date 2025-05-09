from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.pedido_producto import pedido_producto
from app.models.compra import Compra
from app.models.socio import Socio
from app.models.administrador import Administrador
from decimal import Decimal
from datetime import date
from fastapi import HTTPException


carritos = {}

def obtener_carrito(dni: str):
    return carritos.get(dni, {"items": [], "descuento_aplicado": None})


def agregar_producto(db: Session, dni: str, producto_id: int, cantidad: int):
    producto = db.query(Producto).filter_by(id_producto=producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.stock < cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    carrito = obtener_carrito(dni)
    for item in carrito["items"]:
        if item["producto_id"] == producto_id:
            item["cantidad"] += cantidad
            item["subtotal"] = item["precio_unitario"] * item["cantidad"]
            break
    else:
        carrito["items"].append({
            "producto_id": producto.id_producto,
            "nombre": producto.nombre,
            "precio_unitario": producto.precio,
            "cantidad": cantidad,
            "subtotal": producto.precio * cantidad
        })

    carritos[dni] = carrito
    return calcular_totales(carrito)


def actualizar_producto(dni: str, producto_id: int, nueva_cantidad: int):
    carrito = obtener_carrito(dni)
    for item in carrito["items"]:
        if item["producto_id"] == producto_id:
            if nueva_cantidad == 0:
                carrito["items"].remove(item)
            else:
                item["cantidad"] = nueva_cantidad
                item["subtotal"] = item["precio_unitario"] * nueva_cantidad
            break
    carritos[dni] = carrito
    return calcular_totales(carrito)


def aplicar_descuento(db: Session, dni: str, codigo: str):
    carrito = obtener_carrito(dni)
    es_socio = db.query(Socio).filter_by(dni=dni).first()
    es_admin = db.query(Administrador).filter_by(dni=dni).first()

    if codigo == "SOCIO" and not es_socio:
        raise HTTPException(status_code=403, detail="El código SOCIO requiere ser socio activo")
    if codigo == "ADMIN" and not es_admin:
        raise HTTPException(status_code=403, detail="El código ADMIN requiere ser administrador")

    if codigo == "SOCIO":
        carrito["descuento_aplicado"] = "SOCIO"
    elif codigo == "ADMIN":
        carrito["descuento_aplicado"] = "ADMIN"
    else:
        raise HTTPException(status_code=400, detail="Código de descuento no válido")

    carritos[dni] = carrito
    return calcular_totales(carrito)


def calcular_totales(carrito):
    subtotal = sum(item["subtotal"] for item in carrito["items"])
    descuento = Decimal("0.00")

    if carrito.get("descuento_aplicado") == "SOCIO":
        descuento = subtotal * Decimal("0.15")
    elif carrito.get("descuento_aplicado") == "ADMIN":
        descuento = subtotal * Decimal("0.20")

    total = subtotal - descuento
    return {
        "items": carrito["items"],
        "subtotal": subtotal,
        "descuento_aplicado": carrito.get("descuento_aplicado"),
        "total": total.quantize(Decimal("0.01"))
    }


def confirmar_pedido(db: Session, dni: str):
    carrito = obtener_carrito(dni)
    if not carrito["items"]:
        raise HTTPException(status_code=400, detail="El carrito está vacío")

    totales = calcular_totales(carrito)
    pedido = Pedido(
        precio_total=totales["total"],
        descuento=(totales["subtotal"] - totales["total"])
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    for item in carrito["items"]:
        db.add(PedidoProducto(
            pedido_id=pedido.id_pedido,
            producto_id=item["producto_id"],
            cantidad=item["cantidad"]
        ))
        # Actualizar stock
        producto = db.query(Producto).filter_by(id_producto=item["producto_id"]).first()
        if producto.stock < item["cantidad"]:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente de {producto.nombre}")
        producto.stock -= item["cantidad"]

    db.add(Compra(
        dni=dni,
        id_pedido=pedido.id_pedido,
        fecha_compra=date.today(),
        pagado=False
    ))

    db.commit()

    # Limpiar carrito
    carritos[dni] = {"items": [], "descuento_aplicado": None}
    return {
        "mensaje": "Pedido confirmado con éxito",
        "id_pedido": pedido.id_pedido,
        "total": totales["total"]
    }

