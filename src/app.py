import os
from flask import Flask, json
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import HTTPException

from src.models import db

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
    from src.models import Cliente, Pagamento, Pedido, Produto

    # register blueprints
    from src.controllers import (
        cliente_bp,
        produto_bp,
        pedido_bp,
        pagamento_bp,
        auth_bp,
        role_bp,
    )

    app.register_blueprint(cliente_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(pagamento_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(role_bp)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    return app
