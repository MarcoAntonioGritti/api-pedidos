from http import HTTPStatus

from sqlalchemy import func, inspect

from src.models import Cliente, db
from src.views.cliente import ClienteSchema


def test_get_clientes_success(client, access_token_admin):
    cliente = db.session.execute(db.select(Cliente).where(Cliente.id == 1)).scalar()
    cliente_id = cliente.id

    response = client.get(
        f"/clientes/get/{cliente_id}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    users_schema = ClienteSchema()
    cliente_data = users_schema.dump(cliente)

    assert response.status_code == HTTPStatus.OK
    assert response.json == cliente_data


def test_get_clientes_failure(client, access_token_admin):
    cliente_id = -1

    response = client.get(
        f"/clientes/get/{cliente_id}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    breakpoint()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"message": "Cliente não encontrado!"}
