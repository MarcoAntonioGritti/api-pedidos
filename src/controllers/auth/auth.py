from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token

from src.app import bcrypt
from src.models import Cliente, db

from .blueprint import auth_bp


def _check_valid_password(password_hash, password_raw):
    return bcrypt.check_password_hash(password_hash, password_raw)


@auth_bp.route("/login", methods=["POST"])
def login():
    name = request.json.get("name", None)
    password = request.json.get("password", None)
    cliente = db.session.execute(
        db.select(Cliente).where(Cliente.name == name)
    ).scalar()
    if not cliente or not _check_valid_password(cliente.password, password):
        return {"message": "Bad name or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(cliente.id))
    return {"access_token": access_token}
