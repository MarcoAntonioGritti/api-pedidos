from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Cliente(Base):

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    email: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    data_nascimento: Mapped[date] = mapped_column(sa.Date, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("roles.id"), nullable=False)

    pedidos: Mapped["Pedido"] = relationship(back_populates="cliente")  # type: ignore
    role: Mapped["Role"] = relationship(back_populates="cliente")  # type: ignore

    def __repr__(self) -> str:
        return f"Cliente(id={self.id!r}, name={self.name!r},password={self.password!r}, email={self.email!r}, data_nascimento={self.data_nascimento!r}, role_id={self.role_id})"
