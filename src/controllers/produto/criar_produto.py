from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.models import Produto, db
from src.utils import requires_roles
from src.views.produto import CreateProdutoSchema

from .blueprint import produto_bp


@produto_bp.route("/create", methods=["POST"])
@jwt_required()
@requires_roles("Admin")
def create_produto():
    produto_schema = CreateProdutoSchema()

    try:
        data = produto_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    produto = Produto(
        name=data["name"],
        data_criacao_produto=data["data_criacao_produto"],
        data_vencimento_produto=data["data_vencimento_produto"],
        descricao=data["descricao"],
        categoria=data["categoria"],
        marca=data["marca"],
    )

    db.session.add(produto)
    db.session.commit()

    return {"message": "Produto criado!"}, HTTPStatus.CREATED
