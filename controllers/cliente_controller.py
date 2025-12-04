from extensions import db
from models.cliente import Cliente
from models.codigo_verificacion import CodigoVerificacion
from datetime import datetime, timedelta
import random

class ClienteController:

    @staticmethod
    def login(data):
        correo = data.get("correo")
        password = data.get("password")

        cliente = Cliente.query.filter_by(correo=correo, password=password).first()
        if not cliente:
            return {"error": "Correo o contraseña incorrectos"}, 404

        return {"id": cliente.id, "nombres": cliente.nombres, "correo": cliente.correo}

    @staticmethod
    def save_cliente(data):
        cliente_id = data.get("id", 0)
        nombres = data.get("nombres")
        correo = data.get("correo")
        password = data.get("password")

        if cliente_id == 0:
            if Cliente.query.filter_by(correo=correo).first():
                return {"error": "Correo ya registrado"}, 400
            nuevo = Cliente(nombres=nombres, correo=correo, password=password)
            db.session.add(nuevo)
            db.session.commit()
            return {"id": nuevo.id, "mensaje": "Cliente creado"}
        else:
            cliente = Cliente.query.get(cliente_id)
            if not cliente:
                return {"error": "Cliente no encontrado"}, 404
            cliente.nombres = nombres
            cliente.correo = correo
            cliente.password = password
            db.session.commit()
            return {"id": cliente.id, "mensaje": "Cliente actualizado"}

    @staticmethod
    def generar_codigo(data):
        correo = data.get("correo")
        cliente = Cliente.query.filter_by(correo=correo).first()
        if not cliente:
            return {"error": "Correo no registrado"}, 404

        codigo = str(random.randint(1000, 9999))
        fecha_caducidad = datetime.utcnow() + timedelta(minutes=5)
        nuevo = CodigoVerificacion(id_cliente=cliente.id, codigo=codigo, fecha_caducidad=fecha_caducidad)
        db.session.add(nuevo)
        db.session.commit()
        return {"id": cliente.id, "codigo": codigo, "mensaje": "Código válido por 5 minutos"}

    @staticmethod
    def validar_codigo(data):
        cliente_id = data.get("id")
        codigo = data.get("codigo")
        registro = CodigoVerificacion.query.filter_by(id_cliente=cliente_id, codigo=codigo).first()
        if not registro:
            return {"error": "Código incorrecto"}, 404

        minutos_restantes = (registro.fecha_caducidad - datetime.utcnow()).total_seconds() / 60
        if minutos_restantes < 0:
            return {"error": "Código expirado"}, 400

        return {"mensaje": "Código válido", "minutos_restantes": round(minutos_restantes)}
