from flask import Blueprint, request
from controllers.cliente_controller import ClienteController

cliente_bp = Blueprint("clientes", __name__, url_prefix="/api/clientes")

@cliente_bp.post("/login")
def login():
    return ClienteController.login(request.json)

@cliente_bp.post("/save")
def save_cliente():
    return ClienteController.save_cliente(request.json)

@cliente_bp.post("/codigo")
def generar_codigo():
    return ClienteController.generar_codigo(request.json)

@cliente_bp.post("/codigo/validar")
def validar_codigo():
    return ClienteController.validar_codigo(request.json)
