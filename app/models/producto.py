# Modelo Producto

# Importo la instancia de SQLAlchemy
from app import db

# Defino como que sean los atributos de producto y con db.Model le dice a SQLAlchemy que corresponde a una tabla de una base de datos
class Producto(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    # Hace que cuando imprimamos un producto por terminal se vea asi --> <Producto Camisa>
    # __repr__ --> es un método especial de Python, controla cómo se va a imprimir o a representar el objeto cuando 
    # lo vemos en la terminal
    def __repr__(self):
        return f"<Producto {self.nombre}"