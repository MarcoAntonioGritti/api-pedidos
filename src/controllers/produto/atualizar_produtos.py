from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import inspect
from werkzeug.exceptions import NotFound

from src.models import Produto, db
from src.utils import requires_roles
from src.views.produto import UpdateProdutoSchema

from .blueprint import produto_bp


@produto_bp.route("/update/<int:id>", methods=["PATCH"])
@jwt_required()
@requires_roles("Admin")
def update_produto(id):
    try:
        produto = db.get_or_404(Produto, id)
    except NotFound:
        return {"error": "Produto não encontrado"}, HTTPStatus.NOT_FOUND

    produto_schema = UpdateProdutoSchema()

    try:
        data = produto_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    mapper = inspect(Produto)
    for column in mapper.attrs:
        if column.key in data:
            setattr(produto, column.key, data[column.key])

    db.session.commit()

    return {"message": "Produto atualizado!"}, HTTPStatus.OK
