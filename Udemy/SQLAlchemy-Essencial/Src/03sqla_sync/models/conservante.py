import sqlalchemy as sa

from sqlalchemy import orm
from typing import List
from sqlalchemy.orm import Mapped
from datetime import datetime

from models.model_base import ModelBase
from models.join_tables import conservantes_picole


class Conservante(ModelBase):
    __tablename__: str = 'conservantes'

    id: int = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    
    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    descricao: str = sa.Column(sa.String(45), nullable=False)

    #picoles: Mapped[List["Picole"]] = orm.relationship(
    #    'Picole',
    #    secondary=conservantes_picole,
    #    back_populates='conservantes'
    #)

    def __repr__(self) -> str:
        return f'<Conservante: {self.nome}>'

