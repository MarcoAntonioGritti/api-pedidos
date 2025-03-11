from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Pedido(Base):

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    data: Mapped[date] = mapped_column(sa.Date, nullable=False)
    cliente_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("clientes.id"), nullable=False
    )
    produto_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("produtos.id"), nullable=False
    )
    valor_pedido: Mapped[float] = mapped_column(sa.Float, nullable=False)

    quantidade: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    pagamento_efetuado: Mapped[bool] = mapped_column(sa.Boolean, default=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="pedidos")  # type: ignore
    produto: Mapped["Produto"] = relationship(back_populates="pedido")  # type: ignore
    pagamento: Mapped["Pagamento"] = relationship(back_populates="pedido", uselist=False)  # type: ignore

    def __repr__(self) -> str:
        return f"Pedido(id={self.id!r}, cliente_id={self.cliente_id!r}, produto_id={self.produto_id!r},valor_pedido={self.valor_pedido!r} ,quantidade={self.quantidade!r}, data={self.data!r}, pagamento_efetuado={self.pagamento_efetuado!r})"
