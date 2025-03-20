from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.models import Pedido, db
from src.views.pedido import CreatePedidoSchema

from .blueprint import pedido_bp


@pedido_bp.route("/create", methods=["POST"])
@jwt_required()
def create_pedido():
    pedido_schema = CreatePedidoSchema()

    try:
        data = pedido_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    pedido = Pedido(
        data=data["data"],
        cliente_id=data["cliente_id"],
        produto_id=data["produto_id"],
        valor_pedido=data["valor_pedido"],
        quantidade=data["quantidade"],
    )

    db.session.add(pedido)
    db.session.commit()

    return {"message": "Pedido criado!"}, HTTPStatus.CREATED
