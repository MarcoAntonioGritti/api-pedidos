from http import HTTPStatus

from flask_jwt_extended import jwt_required

from src.models import Cliente, db
from src.utils import requires_roles
from src.views.cliente import ClienteSchema

from .blueprint import cliente_bp


@cliente_bp.route("/list", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def list_clientes():
    try:
        clientes = db.session.execute(db.select(Cliente)).scalars().all()
        return ClienteSchema(many=True).dump(clientes), HTTPStatus.OK
    except Exception:
        return {"message": "Erro ao buscar clientes!"}, HTTPStatus.INTERNAL_SERVER_ERROR
