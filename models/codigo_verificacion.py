from extensions import db
from datetime import datetime

class CodigoVerificacion(db.Model):
    __tablename__ = 'codigo_verificacion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    codigo = db.Column(db.String(4), nullable=False)
    fecha_caducidad = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
