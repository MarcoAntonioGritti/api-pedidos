from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.app import ma
from src.models import Cliente, Role


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True

        name = fields.Str()


class ClienteSchema(SQLAlchemyAutoSchema):
    role = fields.Nested(RoleSchema, only=["name"])

    class Meta:
        model = Cliente
        load_instance = True
        include_fk = True


class CreateClienteSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    data_nascimento = fields.Date(required=True)
    role_id = fields.Int(required=True)


class UpdateClienteSchema(ma.Schema):
    name = fields.String(required=False)
    email = fields.String(required=False)
    password = fields.String(required=False)
    data_nascimento = fields.Date(required=False)
    role_id = fields.Int(required=False)
