from flask import Blueprint, render_template
from app.models.producto import Producto

inicio = Blueprint('inicio', __name__)

@inicio.route('/')
def mostrar_inicio():
    productos = Producto.query.all()
    return render_template('inicio.html', productos=productos)