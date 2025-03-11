from .auth.blueprint import auth_bp
from .cliente.blueprint import cliente_bp
from .pagamento.blueprint import pagamento_bp
from .pedido.blueprint import pedido_bp
from .produto.blueprint import produto_bp
from .role.blueprint import role_bp

__all__ = [
    "cliente_bp",
    "produto_bp",
    "pedido_bp",
    "pagamento_bp",
    "auth_bp",
    "role_bp",
]
