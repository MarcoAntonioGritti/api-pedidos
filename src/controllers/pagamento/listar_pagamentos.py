from http import HTTPStatus

from flask_jwt_extended import jwt_required

from src.models import Pagamento, db
from src.utils import requires_roles
from src.views.pagamento import PagamentoSchema

from .blueprint import pagamento_bp


@pagamento_bp.route("/list", methods=["GET"])
@requires_roles("Admin")
@jwt_required()
def list_pagamentos():
    try:
        pagamentos = db.session.query(Pagamento).all()
        result = PagamentoSchema(many=True).dump(pagamentos)
        return result, HTTPStatus.OK
    except Exception as exc:
        return {"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR
