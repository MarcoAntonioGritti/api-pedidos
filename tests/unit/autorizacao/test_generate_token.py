from http import HTTPStatus

import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

# Importa a rota de login para testar
from src.controllers.auth.auth import login
from src.models import Cliente


@pytest.fixture
def app():
    """Cria um app Flask de teste."""
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret"  # Chave secreta para JWT
    jwt = JWTManager(app)
    return app


def test_login_success(mocker, app):
    """Teste de login bem-sucedido."""
    # Cria um cliente falso para o teste
    mock_cliente = Cliente(id=1, name="marquinhos", password="hashed_password")

    # Mock do bcrypt para validar a senha corretamente
    mocker.patch("src.app.bcrypt.check_password_hash", return_value=True)

    # Mock do banco para retornar o cliente falso
    mocker.patch(
        "src.models.db.session.execute",
        return_value=mocker.Mock(scalar=lambda: mock_cliente),
    )

    with app.app_context():  # Adiciona o contexto do app
        with app.test_request_context(json={"name": "marquinhos", "password": "1234"}):
            response = login()  # Chama a função de login

    # Verifica se o status da resposta é OK e se o token de acesso está presente
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json


def test_login_fail_invalid_credentials(mocker, app):
    """Teste de login com credenciais inválidas."""
    # Mock do banco para retornar None, simulando credenciais inválidas
    mocker.patch(
        "src.models.db.session.execute", return_value=mocker.Mock(scalar=lambda: None)
    )

    with app.app_context():  # Adiciona o contexto do app
        with app.test_request_context(json={"name": "marquinhos", "password": "1234"}):
            response = login()  # Chama a função de login

    # Verifica se o status da resposta é UNAUTHORIZED e se a mensagem de erro está correta
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {"message": "Bad name or password"}
