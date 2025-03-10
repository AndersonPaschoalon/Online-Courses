from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped

from models.model_base import ModelBase
from models.tipo_picole import TipoPicole


class Lote(ModelBase):
    __tablename__: str = "lotes"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    id_tipo_picole: int = sa.Column(sa.Integer, sa.ForeignKey("tipos_picole.id"))
    tipo_picole: Mapped["TipoPicole"] = orm.relationship("TipoPicole", lazy="joined")

    quantidade: int = sa.Column(sa.Integer, nullable=False)

    def __repr__(self) -> str:
        return (
            f"Lote("
            f"id={self.id}, "
            f"data_criacao={self.data_criacao}, "
            f"id_tipo_picole={self.id_tipo_picole}, "
            f"quantidade={self.quantidade}, "
            f")"
        )
