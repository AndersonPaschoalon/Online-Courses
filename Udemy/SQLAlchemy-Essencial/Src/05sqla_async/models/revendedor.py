from datetime import datetime

import sqlalchemy as sa

from models.model_base import ModelBase


class Revendedor(ModelBase):
    __tablename__: str = "revendedores"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    cnpj: str = sa.Column(sa.String(45), unique=True, nullable=False)
    razao_social: str = sa.Column(sa.String(100), nullable=False)
    contato: str = sa.Column(sa.String(100), nullable=False)

    def __repr__(self) -> str:
        return (
            f"Revendedor("
            f"id={self.id}, "
            f"data_criacao={self.data_criacao}, "
            f"cnpj={self.cnpj}, "
            f"razao_social={self.razao_social}, "
            f"contato={self.contato}, "
            f")"
        )
