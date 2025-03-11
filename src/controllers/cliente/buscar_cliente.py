from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Cliente, db
from src.utils import requires_roles
from src.views.cliente import ClienteSchema

from .blueprint import cliente_bp


@cliente_bp.route("/get/<int:id>", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def get_cliente(id):
    try:
        cliente = db.get_or_404(Cliente, id)
        return ClienteSchema().dump(cliente), HTTPStatus.OK
    except NotFound:
        return {"message": "Cliente não encontrado!"}, HTTPStatus.NOT_FOUND
