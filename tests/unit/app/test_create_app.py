from flask import Flask


def test_create_app(app):
    # Vefificando se a app dada, retorna um instância do Flask
    assert isinstance(app, Flask)

    # Verificando se configurações de ambiente estão corretas
    assert app.config["SECRET_KEY"] == "test"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"
    assert app.config["JWT_SECRET_KEY"] == "super-test"

    # Verificando se os bluenprints, estão registrados na minha aplicação
    assert "cliente" in app.blueprints
    assert "produto" in app.blueprints
    assert "pedido" in app.blueprints
    assert "pagamento" in app.blueprints
    assert "auth" in app.blueprints
    assert "role" in app.blueprints
    assert "pix" in app.blueprints
