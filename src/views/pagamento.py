from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.app import ma
from src.models import Pagamento, Pedido


class PedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido
        load_instance = True
        include_fk = True

    cliente_id = fields.Integer()
    produto_id = fields.Integer()
    data = fields.Date()


class PagamentoSchema(SQLAlchemyAutoSchema):
    pedido = fields.Nested(PedidoSchema, only=("cliente_id", "produto_id", "data"))

    class Meta:
        model = Pagamento
        load_instance = True


class CreatePagamentoSchema(ma.Schema):
    pedido_id = fields.Integer(required=True)
    valor = fields.Float(required=True)
    data_pagamento = fields.Date(required=True)
