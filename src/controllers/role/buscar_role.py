from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Role, db
from src.utils import requires_roles
from src.views.role import RoleSchema

from .blueprint import role_bp


@role_bp.route("/get/<int:id>", methods=["GET"])
@requires_roles("Admin")
@jwt_required()
def get_role(id):
    try:
        role = db.get_or_404(Role, id)
        return RoleSchema().dump(role), HTTPStatus.OK
    except NotFound:
        return {"message": "Role não encontrada!"}, HTTPStatus.NOT_FOUND
