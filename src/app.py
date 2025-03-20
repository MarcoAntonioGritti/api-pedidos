import os

from src.exceptions import CustomErrorException
from flask import Flask, json, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException
from datetime import datetime
from src.models import Cliente, Role, db
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect

# instances
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()


def create_app(environment=os.environ["ENVIRONMENT"]):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)  # Garante a criação das pastas
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)

    # import models
    # register blueprints
    from src.controllers import (
        auth_bp,
        cliente_bp,
        pagamento_bp,
        pedido_bp,
        produto_bp,
        role_bp,
        pix_bp,
    )
    from src.models import Cliente, Pagamento, Pedido, Produto, Pix

    app.register_blueprint(cliente_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(pagamento_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(pix_bp)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # Verifica se a exceção é uma CustomErrorException
        if isinstance(e, CustomErrorException):
            # Se for, retorna a mensagem personalizada e o código de status fornecido
            response = jsonify({"message": e.message})
            response.status_code = e.code
        else:
            # Se não for, mantém a resposta padrão
            response = e.get_response()
            # Substitui o corpo com o formato JSON padrão para a exceção
            response.data = json.dumps(
                {
                    "code": e.code,
                    "name": e.name,
                    "description": e.description,
                }
            )
            response.content_type = "application/json"

        return response

        # Criar admin somente se o banco estiver pronto

    with app.app_context():
        ensure_admin_created()

    return app


def ensure_admin_created():
    """Verifica se as tabelas existem e cria o usuário admin."""
    try:
        # Verifica se a tabela Role existe antes de tentar acessar os dados
        inspector = inspect(db.engine)
        if inspector.has_table("roles") and inspector.has_table("clientes"):
            create_default_admin()
    except OperationalError:
        print("⚠️ Banco de dados ainda não está pronto. Ignorando criação do admin.")


def create_default_admin():
    """Cria o usuário admin se ele não existir."""
    with db.session.begin():
        admin_role = Role.query.filter_by(name="Admin").first()
        if not admin_role:
            admin_role = Role(name="Admin", descricao="Administrator role")
            db.session.add(admin_role)
            db.session.flush()  # Garante que admin_role.id esteja disponível

        admin_user = Cliente.query.filter_by(email="admin@example.com").first()
        if not admin_user:
            hashed_password = bcrypt.generate_password_hash("admin123").decode("utf-8")
            data_nascimento = datetime.strptime("2000-01-01", "%Y-%m-%d").date()

            admin_user = Cliente(
                name="Admin",
                email="admin@example.com",
                password=hashed_password,
                data_nascimento=data_nascimento,
                role_id=admin_role.id,
            )
            db.session.add(admin_user)

    db.session.commit()
