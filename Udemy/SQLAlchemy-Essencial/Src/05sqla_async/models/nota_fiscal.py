from datetime import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped

from models.join_tables import lotes_nota_fiscal
from models.lote import Lote
from models.model_base import ModelBase
from models.revendedor import Revendedor


class NotaFiscal(ModelBase):
    __tablename__: str = "notas_fiscais"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    valor: float = sa.Column(sa.DECIMAL(8, 2), nullable=False)
    numero_serie: str = sa.Column(sa.String(45), unique=True, nullable=False)
    descricao: str = sa.Column(sa.String(200), nullable=False)

    id_revendedor: int = sa.Column(sa.Integer, sa.ForeignKey("revendedores.id"))
    revendedor: Mapped["Revendedor"] = orm.relationship("Revendedor", lazy="joined")

    # Uma nota fiscal pode ter vários lotes e um lote está ligado a uma nota fiscal
    lotes: Mapped[List["Lote"]] = orm.relationship(
        "Lote", secondary=lotes_nota_fiscal, backref="lote", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return (
            f"NotaFiscal("
            f"id={self.id}, "
            f"data_criacao={self.data_criacao}, "
            f"valor={self.valor}, "
            f"numero_serie={self.numero_serie}, "
            f"descricao={self.descricao}, "
            f"id_revendedor={self.id_revendedor}, "
            f")"
        )
