from datetime import date

import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from src.models import Base


class Pagamento(Base):

    __tablename__ = "pagamentos"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("pedidos.id"), nullable=False
    )
    valor: Mapped[float] = mapped_column(sa.Float, nullable=False)
    data_pagamento: Mapped[date] = mapped_column(sa.Date, nullable=False)
    chave_pix: Mapped[str] = mapped_column(sa.String, nullable=False)
    pix_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("pixes.id"), nullable=False
    )

    pedido: Mapped["Pedido"] = relationship(back_populates="pagamento")  # type:ignore
    pix: Mapped["Pix"] = relationship(  # type:ignore
        back_populates="pagamento", uselist=False
    )

    def __repr__(self) -> str:
        return f"Pagamento(id={self.id!r}, pedido_id={self.pedido_id!r}, valor={self.valor!r}, data_pagamento={self.data_pagamento!r}, chave_pix={self.chave_pix!r})"


@event.listens_for(Pagamento, "after_insert")
def after_insert_listener(mapper, connection, target):
    from src.models import Pedido

    # Criando uma nova sessão
    with Session(connection) as session:
        pedido = session.query(Pedido).filter_by(id=target.pedido_id).one()
        pedido.pagamento_efetuado = True
        session.commit()
