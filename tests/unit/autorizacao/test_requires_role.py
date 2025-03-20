from http import HTTPStatus

from src.utils import requires_roles


def test_requires_roles_success(mocker):
    mock_user = mocker.Mock()  # Cria um objeto mock
    mock_user.role.name = "Admin"  # Define o atributo role.name do mock como "Admin"

    # Mocka a função get_jwt_identity
    mocker.patch("src.utils.get_jwt_identity")

    # Mocka a função db.get_or_404 para retornar o mock_user
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    # Decora uma função lambda com requires_roles, que só retornará "success" se a role for "Admin"
    decorated_function = requires_roles("Admin")(lambda: "success")

    # Executa a função decorada
    result = decorated_function()

    # Verifica se o resultado é "success"
    assert result == "success"


def test_requires_roles_fail(mocker):
    mock_user = mocker.Mock()  # Cria um objeto mock
    mock_user.role.name = "normal"  # Define o atributo role.name do mock como "normal"

    # Mocka a função get_jwt_identity
    mocker.patch("src.utils.get_jwt_identity")

    # Mocka a função db.get_or_404 para retornar o mock_user
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    # Decora uma função lambda com requires_roles, que só retornará "success" se a role for "Admin"
    decorated_function = requires_roles("Admin")(lambda: "success")

    # Executa a função decorada
    result = decorated_function()

    # Verifica se o resultado é uma mensagem de acesso negado com status HTTP 403
    assert result == (
        {"message": "Cliente não possui accesso."},
        HTTPStatus.FORBIDDEN,
    )
