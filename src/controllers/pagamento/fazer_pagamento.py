from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.models import Pagamento, Pedido, db
from src.utils import requires_roles
from src.views.pagamento import CreatePagamentoSchema

from .blueprint import pagamento_bp


@pagamento_bp.route("/create", methods=["POST"])
@requires_roles("Admin")
@jwt_required()
def create_pagamento():
    pagamento_schema = CreatePagamentoSchema()

    try:
        data = pagamento_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    pedido_id = data["pedido_id"]
    valor_pagamento = data["valor"]

    pedido = Pedido.query.get(pedido_id)

    if not pedido:
        return {"message": "Pedido não encontrado!"}, HTTPStatus.NOT_FOUND

    if valor_pagamento < pedido.valor_pedido or valor_pagamento > pedido.valor_pedido:
        return {
            "message": "Valor do pagamento é menor ou maior que o valor do pedido!"
        }, HTTPStatus.BAD_REQUEST

    pagamento = Pagamento(
        pedido_id=data["pedido_id"],
        valor=data["valor"],
        data_pagamento=data["data_pagamento"],
    )

    db.session.add(pagamento)
    db.session.commit()

    return {"message": "Pagamento Efetuado!"}, HTTPStatus.CREATED
