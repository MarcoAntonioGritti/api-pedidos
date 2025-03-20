from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Pix, db
from src.utils import requires_roles
from src.views.pix import PixSchema

from .blueprint import pix_bp


@pix_bp.route("/consultar-pix/<int:id>", methods=["GET"])
@jwt_required()
@requires_roles("Admin")
def get_pix(id):
    try:
        role = db.get_or_404(Pix, id)
        return PixSchema().dump(role), HTTPStatus.OK
    except NotFound:
        return {"message": "Pix não encontrado!"}, HTTPStatus.NOT_FOUND
