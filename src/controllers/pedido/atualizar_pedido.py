from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.models import Pedido, db
from src.utils import requires_roles
from src.views.pedido import UpdatePedidoSchema

from .blueprint import pedido_bp


@pedido_bp.route("/update/<int:id>", methods=["PATCH"])
@jwt_required()
@requires_roles("Admin")
def update_pedido(id):
    pedido = db.get_or_404(Pedido, id)

    pedido_schema = UpdatePedidoSchema()

    try:
        data = pedido_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    for key, value in data.items():
        setattr(pedido, key, value)

    db.session.commit()

    return {"message": "Pedido atualizado!"}, HTTPStatus.OK
