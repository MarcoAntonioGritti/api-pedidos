from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Role, db
from src.utils import requires_roles

from .blueprint import role_bp


@role_bp.route("/delete/<int:id>", methods=["DELETE"])
@requires_roles("Admin")
@jwt_required()
def delete_role(id):
    try:
        role = db.get_or_404(Role, id)
        db.session.delete(role)
        db.session.commit()
        return {"message": "Roel deletado!"}, HTTPStatus.NO_CONTENT
    except NotFound:
        return {"message": "Role não encontrada!"}, HTTPStatus.NOT_FOUND
