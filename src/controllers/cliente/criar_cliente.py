from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.app import bcrypt
from src.models import Cliente, db
from src.utils import requires_roles
from src.views.cliente import CreateClienteSchema

from .blueprint import cliente_bp


@cliente_bp.route("/create", methods=["POST"])
def create_cliente():
    cliente_schema = CreateClienteSchema()

    try:
        data = cliente_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    cliente = Cliente(
        name=data["name"],
        email=data["email"],
        password=bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
        data_nascimento=data["data_nascimento"],
        role_id=data["role_id"],
    )

    db.session.add(cliente)
    db.session.commit()

    return {"message": "Cliente criado!"}, HTTPStatus.CREATED
