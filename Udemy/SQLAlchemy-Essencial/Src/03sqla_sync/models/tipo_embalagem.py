from datetime import datetime

import sqlalchemy as sa

from models.model_base import ModelBase


class TipoEmbalagem(ModelBase):
    __tablename__: str = "tipos_embalagem"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)

    def __repr__(self) -> str:
        return (
            f"TipoEmbalagem("
            f"id={self.id}, "
            f"data_criacao={self.data_criacao}, "
            f"nome={self.nome}, "
            f")"
        )
