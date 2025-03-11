from http import HTTPStatus

from flask_jwt_extended import jwt_required

from src.models import Produto, db
from src.utils import requires_roles
from src.views.produto import ProdutoSchema

from .blueprint import produto_bp


@produto_bp.route("/list", methods=["GET"])
@requires_roles("Admin")
@jwt_required()
def list_produtos():
    try:
        produtos = db.session.execute(db.select(Produto)).scalars().all()
        return ProdutoSchema(many=True).dump(produtos), HTTPStatus.OK
    except Exception as exc:
        return {"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR
