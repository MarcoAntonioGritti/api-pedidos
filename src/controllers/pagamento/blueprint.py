from flask import Blueprint

# Definição do Blueprint
pagamento_bp = Blueprint("pagamento", __name__, url_prefix="/pagamentos")

# Importar as rotas para registrá-las no Blueprint
from .fazer_pagamento import create_pagamento
from .listar_pedidos_nao_pagos import list_pagamentos_nao_pagos
from .listar_pedidos_pagos import list_pedidos_pagos
