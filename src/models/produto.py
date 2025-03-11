from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Produto(Base):

    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    data_criacao_produto: Mapped[date] = mapped_column(sa.Date, nullable=False)
    data_vencimento_produto: Mapped[date] = mapped_column(sa.Date, nullable=False)
    descricao: Mapped[str] = mapped_column(sa.String, nullable=False)
    categoria: Mapped[str] = mapped_column(sa.String, nullable=False)
    marca: Mapped[str] = mapped_column(sa.String, nullable=False)

    pedido: Mapped["Pedido"] = relationship(back_populates="produto")  # type:ignore

    def __repr__(self) -> str:
        return f"Produto(id={self.id!r}, name={self.name!r},data_criacao_produto={self.data_criacao_produto!r},data_criacao_produto={self.data_criacao_produto!r}, descricao={self.descricao!r}, categoria={self.categoria!r}, marca={self.marca!r})"
