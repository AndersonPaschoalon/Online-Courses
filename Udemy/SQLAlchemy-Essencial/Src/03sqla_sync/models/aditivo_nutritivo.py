import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase


class AditivoNutritivo(ModelBase):
    __tablename__ = 'aditivos_nutritivos'

    id: int = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    node: str = sa.Column(sa.String(45), unique=True, nullable=False)
    formula_quimica: str = sa.Column(sa.String(80), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'AditivoNutritivo(node={self.node}, formula_quimica={self.formula_quimica})'

