from flask import Blueprint

pix_bp = Blueprint("pix", __name__, url_prefix="/pix")

from .consultar_pix import get_pix
from .deletar_pix import delete_pix
from .gerar_pix import gerar_chave_pix
