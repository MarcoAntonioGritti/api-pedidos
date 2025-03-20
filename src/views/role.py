from marshmallow import fields

from src.app import ma
from src.models import Role


class RoleSchema(ma.SQLAlchemySchema):
    id = fields.Int()
    name = fields.Str()
    descricao = fields.Str()

    class Meta:
        model = Role
        load_instance = True


class CreateRoleSchema(ma.Schema):
    name = fields.String(required=True)
    descricao = fields.String(required=True)


class UpdateRoleSchema(ma.Schema):
    name = fields.String(required=False)
    descricao = fields.String(required=False)
