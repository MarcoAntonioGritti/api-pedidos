from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.app import ma
from src.models import Produto


class ProdutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Produto
        load_instance = True


class CreateProdutoSchema(ma.Schema):
    name = fields.String(required=True)
    data_criacao_produto = fields.Date(required=True)
    data_vencimento_produto = fields.Date(required=True)
    descricao = fields.String(required=True)
    categoria = fields.String(required=True)
    marca = fields.String(required=True)


class UpdateProdutoSchema(ma.Schema):
    name = fields.String(required=False)
    data_criacao_produto = fields.Date(required=False)
    data_vencimento_produto = fields.Date(required=False)
    descricao = fields.String(required=False)
    categoria = fields.String(required=False)
    marca = fields.String(required=False)
