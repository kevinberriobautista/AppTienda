#  Blueprint sirve para organizar las rutas en tu aplicación Flask cuando tienes varias secciones (productos, usuarios, pedidos...)
from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models.producto import Producto


# Aqui creo el Blueprint
# 'productos' es el nombre que le estoy dando
# __name__ sirve para que Flask sepa en qué módulo está
productos = Blueprint('productos', __name__)

# Cuandos es ejecute http://url/productos se ejecutará el metodo lista_productos()
# Listar productos
@productos.route('/productos')
def lista_productos():
    productos = Producto.query.all()  # Consulta todos los productos
    return render_template('lista_productos.html', productos=productos)


# Añadir productos
@productos.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio', type=float)
        stock = request.form.get('stock', type=int)

        if not nombre or precio is None or stock is None:
            error = "Nombre, precio y stock son obligatorios."
            return render_template('nuevo_producto.html', error=error)
        
        producto = Producto(nombre = nombre, descripcion = descripcion, precio = precio, stock = stock)
        db.session.add(producto)
        db.session.commit()

        return redirect(url_for('productos.lista_productos'))
    
    return render_template('nuevo_producto.html')

# Editar productos
@productos.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    # if request.method == 'POST': --> chequea si la peticion es un formulario que se envio con un POST
    # De esta manera obtengo los datos del producto para modificarlos
    if request.method == 'POST':   
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio', type=float)
        stock = request.form.get('stock', type=int)

        # Validar campos obligatorios con los datos recibidos
        if not nombre or precio is None or stock is None:
            error = "Nombre, precio y stock son obligatorios."
            return render_template('editar_producto.html', producto=producto, error=error)
        
        # Asignar los nuevos valores al producto
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock = stock

        db.session.commit()
        return redirect(url_for('productos.lista_productos'))
    
    return render_template('editar_producto.html', producto=producto)


# Eliminar productos
@productos.route('/productos/eliminar/<int:id>', methods=['POST', 'GET'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('productos.lista_productos'))