import secrets
from http import HTTPStatus

from flask import request
from marshmallow import ValidationError

from src.models import Pix, db
from src.views.pix import CreatePixSchema

from .blueprint import pix_bp


@pix_bp.route("/gerar-pix", methods=["POST"])
def gerar_chave_pix():
    chave = secrets.token_urlsafe(32)

    pix_schema = CreatePixSchema()

    try:
        data = pix_schema.load(request.json)
        print("VALORES REQ: ", data)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_CONTENT

    pix = Pix(chave=chave, pedido_id=data["pedido_id"])
    print("Pix: ", pix)

    db.session.add(pix)
    db.session.commit()

    return {"Chave": chave}, HTTPStatus.OK
