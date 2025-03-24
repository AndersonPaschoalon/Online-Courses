from datetime import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped

from models.join_tables import (
    aditivos_nutritivos_picole,
    conservantes_picole,
    ingredientes_picole,
    lotes_nota_fiscal,
)
from models.model_base import ModelBase


class Ingrediente(ModelBase):
    __tablename__: str = "ingredientes"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)

    def __repr__(self) -> str:
        return (
            f"Ingrediente("
            f"id={self.id}, "
            f"data_criacao={self.data_criacao}, "
            f"nome={self.nome}, "
            f")"
        )
