from flask import Blueprint

role_bp = Blueprint("role", __name__, url_prefix="/roles")

from .buscar_role import get_role
from .criar_role import create_role
from .deletar_role import delete_role
from .listar_roles import list_role
