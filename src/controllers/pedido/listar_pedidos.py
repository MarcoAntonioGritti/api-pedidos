from http import HTTPStatus

from flask_jwt_extended import jwt_required

from src.models import Pedido, db
from src.utils import requires_roles
from src.views.pedido import PedidoSchema

from .blueprint import pedido_bp


@pedido_bp.route("/list", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def list_pedidos():
    try:
        pedidos = db.session.execute(db.select(Pedido)).scalars().all()
        return PedidoSchema(many=True).dump(pedidos), HTTPStatus.OK
    except Exception:
        return {"message": "Erro ao buscar pedidos!"}, HTTPStatus.INTERNAL_SERVER_ERROR
