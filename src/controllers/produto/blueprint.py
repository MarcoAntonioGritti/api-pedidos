from flask import Blueprint

produto_bp = Blueprint("produto", __name__, url_prefix="/produtos")

from .atualizar_produtos import update_produto
from .buscar_produto import get_produto
from .criar_produto import create_produto
from .deletar_produto import delete_produto
from .listar_produtos import list_produtos
