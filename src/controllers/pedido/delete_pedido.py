from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Pedido, db
from src.utils import requires_roles

from .blueprint import pedido_bp


@pedido_bp.route("/delete/<int:id>", methods=["DELETE"])
@requires_roles("Admin")
@jwt_required()
def delete_pedido(id):
    try:
        pedido = db.get_or_404(Pedido, id)
        db.session.delete(pedido)
        db.session.commit()
        return {"message": "Pedido deletado!"}, HTTPStatus.NO_CONTENT
    except NotFound:
        return {"message": "Pedido não encontrado!"}, HTTPStatus.NOT_FOUND
