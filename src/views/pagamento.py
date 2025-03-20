from marshmallow import fields

from src.app import ma
from src.models import Pagamento, Pedido


class PedidoSchema(ma.SQLAlchemyAutoSchema):
    cliente_id = fields.Integer()
    produto_id = fields.Integer()
    data = fields.Date()
    pagamento_efetuado = fields.Boolean()

    class Meta:
        model = Pedido
        load_instance = True
        include_fk = True


class PagamentoSchema(ma.SQLAlchemyAutoSchema):
    pedido = fields.Nested(
        PedidoSchema, only=("cliente_id", "produto_id", "data", "pagamento_efetuado")
    )

    class Meta:
        model = Pagamento
        include_relationships = True
        load_instance = True


class CreatePagamentoSchema(ma.Schema):
    pedido_id = fields.Integer(required=True)
    valor = fields.Float(required=True)
    data_pagamento = fields.Date(required=True)
    chave_pix = fields.String(required=True)
    pix_id = fields.Integer(required=True)
