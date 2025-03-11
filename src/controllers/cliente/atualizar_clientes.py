from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import inspect
from werkzeug.exceptions import NotFound

from src.models import Cliente, db
from src.utils import requires_roles
from src.views.cliente import UpdateClienteSchema

from .blueprint import cliente_bp


@cliente_bp.route("/update/<int:id>", methods=["PATCH"])
@jwt_required()
@requires_roles("Admin")
def update_cliente(id):
    try:
        cliente = db.get_or_404(Cliente, id)
    except NotFound:
        return {"message": "Cliente não encontrado!"}, HTTPStatus.NOT_FOUND

    cliente_schema = UpdateClienteSchema()

    try:
        data = cliente_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    mapper = inspect(Cliente)
    for column in mapper.attrs:
        if column.key in data:
            setattr(cliente, column.key, data[column.key])

    db.session.commit()

    return {"message": "Cliente atualizado!"}, HTTPStatus.OK
