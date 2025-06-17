# app/routes/carrito.py
from flask import Blueprint, session, render_template, request, redirect, url_for
from app.models.producto import Producto
from app import db

carrito = Blueprint('carrito', __name__)

@carrito.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    # Si carrito es lista, conviértelo a dict vacío para evitar error
    if not isinstance(carrito, dict):
        carrito = {}
    productos_carrito = []

    for id_str, cantidad in carrito.items():
        producto = Producto.query.get(int(id_str))
        if producto:
            productos_carrito.append({
                'producto': producto,
                'cantidad': cantidad
            })
        
    return render_template('carrito.html', productos_carrito=productos_carrito)


@carrito.route('/carrito/agregar/<int:id>', methods=['POST'])
def agregar_al_carrito(id):
    producto = Producto.query.get_or_404(id)
    cantidad = int(request.form.get('cantidad', 1))

    carrito = session.get('carrito', {})

    # Si carrito no es dict (por ejemplo es lista), inicializarlo vacío
    if not isinstance(carrito, dict):
        carrito = {}

    if str(id) in carrito:
        carrito[str(id)] += cantidad
    else:
        carrito[str(id)] = cantidad

    session['carrito'] = carrito
    return redirect(url_for('productos.lista_productos'))


@carrito.route('/carrito/eliminar/<int:id>', methods=['POST'])
def eliminar_del_carrito(id):
    carrito = session.get('carrito', {})
    carrito.pop(str(id), None)
    session['carrito'] = carrito
    return redirect(url_for('carrito.ver_carrito'))

@carrito.route('/comprar', methods=['POST'])
def comprar():
    carrito = session.get('carrito', {})

    # Obtener ids de productos en el carrito
    ids = [int(id_str) for id_str in carrito.keys()]

    productos = Producto.query.filter(Producto.id.in_(ids)).all()

    total = 0
    for producto in productos:
        cantidad = carrito.get(str(producto.id), 0)
        total += producto.precio * cantidad

        # Restar stock considerando la cantidad
        producto.stock -= cantidad
        if producto.stock < 0:
            producto.stock = 0  # para no tener stock negativo

    db.session.commit()

    # Limpiar el carrito
    session['carrito'] = {}

    return render_template('compra_realizada.html', total=total)