from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.app import ma
from src.models import Cliente, Pedido, Produto


class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        load_instance = True
        include_fk = True

    name = fields.Str()
    email = fields.Str()


class ProdutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Produto
        load_instance = True
        include_fk = True

    nome = fields.Str()
    preco = fields.Float()
    data_criacao_produto = fields.Date()
    data_vencimento_pedido = fields.Date()


class PedidoSchema(SQLAlchemyAutoSchema):
    cliente = fields.Nested(ClienteSchema, only=("name", "email"))
    produto = fields.Nested(
        ProdutoSchema,
        only=("name", "preco", "data_criacao_produto", "data_vencimento_produto"),
    )

    class Meta:
        model = Pedido
        load_instance = True


class CreatePedidoSchema(ma.Schema):
    data = fields.Date(required=False)
    cliente_id = fields.Integer(required=True)
    produto_id = fields.Integer(required=True)
    valor_pedido = fields.Float(required=True)
    quantidade = fields.Integer(required=True)


class UpdatePedidoSchema(ma.Schema):
    data = fields.Date(required=False)
    cliente_id = fields.Integer(required=False)
    produto_id = fields.Integer(required=False)
    valor_pedido = fields.Float(required=False)
    quantidade = fields.Integer(required=False)
