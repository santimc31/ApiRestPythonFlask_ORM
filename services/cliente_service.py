from extensions import db
from models.cliente import Cliente
from models.codigo_verificacion import CodigoVerificacion
from datetime import datetime, timedelta
import random

class ClienteService:

    @staticmethod
    def login(correo, password):
        return Cliente.query.filter_by(correo=correo, password=password).first()

    @staticmethod
    def save_cliente(id, nombres, correo, password):
        if id == 0:
            existente = Cliente.query.filter_by(correo=correo).first()
            if existente:
                return {"error": "Correo ya registrado"}

            nuevo = Cliente(nombres=nombres, correo=correo, password=password)
            db.session.add(nuevo)
            db.session.commit()
            return {"insertID": nuevo.id}

        else:
            cliente = Cliente.query.get(id)
            if not cliente:
                return {"error": "Cliente no encontrado"}

            cliente.nombres = nombres
            cliente.correo = correo
            cliente.password = password
            db.session.commit()
            return {"insertID": id}

    @staticmethod
    def generar_codigo(correo):
        cliente = Cliente.query.filter_by(correo=correo).first()
        if not cliente:
            return {"error": "Correo no registrado"}

        codigo = str(random.randint(1000, 9999))
        fecha = datetime.utcnow() + timedelta(minutes=5)

        nuevo = CodigoVerificacion(id_cliente=cliente.id, codigo=codigo, fecha_caducidad=fecha)
        db.session.add(nuevo)
        db.session.commit()

        return {"idCliente": cliente.id, "codigo": codigo}

    @staticmethod
    def validar_codigo(idCliente, codigo):
        registro = CodigoVerificacion.query.filter_by(id_cliente=idCliente, codigo=codigo).first()
        if not registro:
            return {"minutosRestantes": -999}

        minutos = int((registro.fecha_caducidad - datetime.utcnow()).total_seconds() / 60)
        return {"minutosRestantes": minutos}
