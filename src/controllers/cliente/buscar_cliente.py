from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound
from src.exceptions import CustomErrorException
from src.models import Cliente, db
from src.utils import requires_roles
from src.views.cliente import ClienteSchema

from .blueprint import cliente_bp


@cliente_bp.route("/get/<int:id>", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def get_cliente(id):
    cliente = db.session.get(Cliente, id)
    if not cliente:
        # Levanta a exceção personalizada com a mensagem de erro
        raise CustomErrorException("Cliente não encontrado!", HTTPStatus.NOT_FOUND)
    return ClienteSchema().dump(cliente), HTTPStatus.OK
