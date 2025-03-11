from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Cliente, db
from src.utils import requires_roles

from .blueprint import cliente_bp


@cliente_bp.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
@requires_roles("Admin")
def delete_cliente(id):
    try:
        cliente = db.get_or_404(Cliente, id)
        db.session.delete(cliente)
        db.session.commit()
        return {"message": "Cliente deletado!"}, HTTPStatus.NO_CONTENT
    except NotFound:
        return {"message": "Cliente não encontrado!"}, HTTPStatus.NOT_FOUND
