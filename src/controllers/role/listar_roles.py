from http import HTTPStatus

from flask_jwt_extended import jwt_required

from src.models import Role, db
from src.utils import requires_roles
from src.views.role import RoleSchema

from .blueprint import role_bp


@role_bp.route("/list", methods=["GET"])
@requires_roles("Admin")
@jwt_required()
def list_role():
    try:
        roles = db.session.execute(db.select(Role)).scalars().all()
        return RoleSchema(many=True).dump(roles), HTTPStatus.OK
    except Exception:
        return {"message": "Erro ao buscar roles!"}, HTTPStatus.INTERNAL_SERVER_ERROR
