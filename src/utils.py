from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity

from src.models import Cliente, db


def requires_roles(*role_names):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            cliente_id = get_jwt_identity()
            cliente = db.get_or_404(Cliente, cliente_id)

            if cliente.role.name not in role_names:
                return {"message": "Cliente não possui accesso."}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)

        return wrapped

    return decorator
