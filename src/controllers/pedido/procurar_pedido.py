from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Pedido, db
from src.utils import requires_roles
from src.views.pedido import PedidoSchema

from .blueprint import pedido_bp


@pedido_bp.route("/get/<int:id>", methods=["GET"])
@requires_roles("Admin")
@jwt_required()
def get_pedido(id):
    try:
        pedido = db.get_or_404(Pedido, id)
    except NotFound:
        return {"message": "Pedido não encontrado!"}, HTTPStatus.NOT_FOUND

    return PedidoSchema().dump(pedido), HTTPStatus.OK
