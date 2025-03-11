from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Produto, db
from src.utils import requires_roles
from src.views.produto import ProdutoSchema

from .blueprint import produto_bp


@produto_bp.route("/get/<int:id>", methods=["GET"])
@requires_roles("Admin")
@jwt_required()
def get_produto(id):
    try:
        produto = db.get_or_404(Produto, id)
        return ProdutoSchema().dump(produto), HTTPStatus.OK
    except NotFound:
        return {"error": "Produto não encontrado"}, HTTPStatus.NOT_FOUND
