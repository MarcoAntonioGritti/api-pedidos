from http import HTTPStatus

from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from src.models import Pix, db
from src.utils import requires_roles
from src.views.pix import PixSchema

from .blueprint import pix_bp


@pix_bp.route("/listar", methods=["GET"])
def list_pixes():
    try:
        pixes = db.session.execute(db.seletc(Pix)).scalars().all()
        return PixSchema().dump(many=True).dump(pixes), HTTPStatus.OK
    except Exception:
        return {"message": "Erro ao buscar pixes!"}, HTTPStatus.INTERNAL_SERVER_ERROR
