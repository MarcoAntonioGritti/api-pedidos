from flask import Blueprint

pedido_bp = Blueprint("pedido", __name__, url_prefix="/pedidos")

from .atualizar_pedido import update_pedido
from .delete_pedido import delete_pedido
from .fazer_pedido import create_pedido
from .listar_pedidos import list_pedidos
from .procurar_pedido import get_pedido
