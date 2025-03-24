from datetime import datetime
from typing import List

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import Mapped

from models.join_tables import conservantes_picole
from models.model_base import ModelBase


class Conservante(ModelBase):
    __tablename__: str = "conservantes"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    descricao: str = sa.Column(sa.String(45), nullable=False)

    def __repr__(self) -> str:
        return (
            f"Conservante("
            f"id={self.id}, "
            f"data_criacao={self.data_criacao}, "
            f"nome={self.nome}, "
            f"descricao={self.descricao}, "
            f")"
        )
