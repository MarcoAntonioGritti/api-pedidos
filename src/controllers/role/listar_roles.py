from http import HTTPStatus

from flask_jwt_extended import jwt_required

from src.models import Role, db
from src.utils import requires_roles
from src.views.role import RoleSchema

from .blueprint import role_bp


@role_bp.route("/list", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def list_role():
    try:
        roles = db.session.execute(db.select(Role)).scalars().all()
        serialized_roles = RoleSchema(many=True).dump(roles)  # Agora deve funcionar
        print(serialized_roles)  # Confirme se os dados aparecem corretamente
        return serialized_roles, HTTPStatus.OK
    except Exception as e:
        return {
            "message": f"Erro ao buscar roles! {str(e)}"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
