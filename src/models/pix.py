import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Pix(Base):

    __tablename__ = "pixes"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    chave: Mapped[str] = mapped_column(sa.String)

    pedido_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("pedidos.id"), nullable=False, unique=True
    )

    pedido: Mapped["Pedido"] = relationship(back_populates="pix")  # type: ignore
    pagamento: Mapped["Pagamento"] = relationship(back_populates="pix")  # type:ignore

    def __repr__(self) -> str:
        return f"Pix(id={self.id!r}, chave{self.chave!r}, pedido_id{self.pedido_id!r})"
