from http import HTTPStatus

from flask_jwt_extended import jwt_required

from src.models import Pagamento, Pedido, db
from src.utils import requires_roles
from src.views.pagamento import PagamentoSchema

from .blueprint import pagamento_bp


@pagamento_bp.route("/list/pagos", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def list_pagamentos_pagos():
    try:
        pagamentos = (
            db.session.query(Pagamento)
            .join(Pedido)
            .filter(Pedido.pagamento_efetuado == True)
            .all()
        )
        result = PagamentoSchema(many=True).dump(pagamentos)
        return result, HTTPStatus.OK
    except Exception as exc:
        return {"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR
