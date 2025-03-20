from http import HTTPStatus

from werkzeug.exceptions import NotFound

from src.models import Pix, db

from .blueprint import pix_bp


@pix_bp.route("/deletar/<int:id>", methods=["DELETE"])
def delete_pix(id):
    try:
        pix = db.get_or_404(Pix, id)
        db.session.delete(pix)
        db.session.commit()
        return {"message": "Cliente deletado!"}, HTTPStatus.NO_CONTENT
    except NotFound:
        return {"message": "Cliente não encontrado!"}, HTTPStatus.NOT_FOUND
