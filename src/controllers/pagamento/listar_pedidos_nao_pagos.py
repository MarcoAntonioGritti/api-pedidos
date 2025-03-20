from http import HTTPStatus

from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload

from src.models import Pagamento, Pedido, db
from src.utils import requires_roles
from src.views.pagamento import PedidoSchema

from .blueprint import pagamento_bp


@pagamento_bp.route("/listar-pedidos-nao-pagos", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def list_pagamentos_nao_pagos():
    try:
        pedido_nao_pago = (
            db.session.execute(
                db.select(Pedido).where(Pedido.pagamento_efetuado == False)
            )
            .scalars()
            .all()
        )
        print(
            "Pedidos não pagos:", pedido_nao_pago
        )  # Verifique se a lista contém objetos
        result = PedidoSchema(many=True).dump(pedido_nao_pago)
        return result, HTTPStatus.OK
    except Exception as exc:
        return {"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR
