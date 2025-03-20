from marshmallow import fields

from src.app import ma
from src.models import Pedido, Pix


class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido
        load_instace = True
        include_fk = True

    cliente_id = fields.Int()
    produto_id = fields.Int()
    valor_pedido = fields.Float()


class PixSchema(ma.SQLAlchemyAutoSchema):
    pedido = fields.Nested(
        PedidoSchema, only=("cliente_id", "produto_id", "valor_pedido")
    )

    class Meta:
        model = Pix
        load_instace = True
        include_fk = True


class CreatePixSchema(ma.Schema):

    chave = fields.Str(required=False)
    pedido_id = fields.Int(required=True)
