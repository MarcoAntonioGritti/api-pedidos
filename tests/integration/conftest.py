import pytest
import secrets
from datetime import datetime
from src.app import create_app
from src.models import Cliente, Role, db, Produto, Pedido, Pix, Pagamento
from src.app import bcrypt


@pytest.fixture()
def app():
    # Cria a aplicação (usará o ambiente definido pela variável de ambiente)
    app = create_app("testing")

    # Entra no contexto da aplicação
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados
        yield app  # Retorna a aplicação para o teste


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def role_admin():
    # Cria uma role admin
    role_admin = Role(name="Admin", descricao="teste test")
    db.session.add(role_admin)
    db.session.commit()
    return role_admin


@pytest.fixture()
def cliente_fixture(role_admin):
    # Cria um usuário admin com a role admin e data de nascimento
    hashed_password = bcrypt.generate_password_hash("admin123").decode("utf-8")
    role_id = role_admin.id
    admin = Cliente(
        name="admin",
        email="teste@hotmail.com",
        password=hashed_password,
        data_nascimento=datetime.strptime("1990-01-01", "%Y-%m-%d").date(),
        role_id=role_id,
    )
    db.session.add(admin)
    db.session.commit()
    return admin


@pytest.fixture()
def access_token_admin(client, cliente_fixture):
    # Faz login com o usuário admin para obter o token de acesso
    response = client.post(
        "/auth/login", json={"name": "admin", "password": "admin123"}
    )
    access_token = response.json["access_token"]
    return access_token


@pytest.fixture()
def produto():
    # Cria um produto com os campos especificados
    produto = Produto(
        name="Produto Teste",
        data_criacao_produto=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
        data_vencimento_produto=datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
        descricao="Descrição do produto teste",
        categoria="Categoria Teste",
        marca="Marca Teste",
    )
    db.session.add(produto)
    db.session.commit()
    return produto


@pytest.fixture()
def pedido(cliente_fixture, produto):
    # Cria um pedido com os campos especificados
    pedido = Pedido(
        data=datetime.strptime("2023-10-01", "%Y-%m-%d").date(),
        cliente_id=cliente_fixture.id,
        produto_id=produto.id,
        valor_pedido=100.0,
        quantidade=2,
        pagamento_efetuado=False,
    )
    db.session.add(pedido)
    db.session.commit()
    return pedido


@pytest.fixture()
def pix(pedido):
    # Cria um pix com o campo especificado
    chave = secrets.token_urlsafe(32)

    pix = Pix(chave=chave, pedido_id=pedido.id)
    db.session.add(pix)
    db.session.commit()
    return pix


@pytest.fixture()
def pagamento(pix):
    # Cria um pagamento com os campos especificados
    pagamento = Pagamento(
        valor=100.0,
        data_pagamento=datetime.strptime("2023-10-02", "%Y-%m-%d").date(),
        chave_pix=pix.chave,  # Usa a chave_pix gerada em pix
        pix_id=pix.id,
    )
    db.session.add(pagamento)
    db.session.commit()
    return pagamento
