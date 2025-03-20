from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.models import Role, db
from src.utils import requires_roles
from src.views.role import CreateRoleSchema

from .blueprint import role_bp


@role_bp.route("/create", methods=["POST"])
@jwt_required()
@requires_roles("Admin")
def create_role():
    role_schema = CreateRoleSchema()

    try:
        data = role_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    role = Role(name=data["name"], descricao=data["descricao"])

    db.session.add(role)
    db.session.commit()

    return {"message": "Role criado!"}, HTTPStatus.CREATED
