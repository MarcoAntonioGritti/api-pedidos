from flask import Blueprint

cliente_bp = Blueprint("cliente", __name__, url_prefix="/clientes")

from .atualizar_clientes import update_cliente
from .buscar_cliente import get_cliente
from .criar_cliente import create_cliente
from .deletar_cliente import delete_cliente
from .listar_clientes import list_clientes
