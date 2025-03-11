from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Produto, db
from src.utils import requires_roles

from .blueprint import produto_bp


@produto_bp.route("/delete/<int:id>", methods=["DELETE"])
@requires_roles("Admin")
@jwt_required()
def delete_produto(id):
    try:
        produto = db.get_or_404(Produto, id)
        db.session.delete(produto)
        db.session.commit()
        return {"message": "Produto deletado!"}, HTTPStatus.NO_CONTENT
    except NotFound:
        return {"error": "Produto não encontrado"}, HTTPStatus.NOT_FOUND
