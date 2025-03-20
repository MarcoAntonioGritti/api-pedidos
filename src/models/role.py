import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    descricao: Mapped[str] = mapped_column(sa.String, nullable=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="role")  # type:ignore

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r},descricao={self.descricao!r}"
