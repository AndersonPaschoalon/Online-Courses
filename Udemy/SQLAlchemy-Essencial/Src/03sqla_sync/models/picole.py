from datetime import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped

from models.aditivo_nutritivo import AditivoNutritivo
from models.conservante import Conservante
from models.ingrediente import Ingrediente
from models.join_tables import (
    aditivos_nutritivos_picole,
    conservantes_picole,
    ingredientes_picole,
)
from models.model_base import ModelBase
from models.sabor import Sabor
from models.tipo_embalagem import TipoEmbalagem
from models.tipo_picole import TipoPicole


class Picole(ModelBase):
    __tablename__: str = "picoles"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    preco: float = sa.Column(sa.DECIMAL(8, 2), nullable=False)

    id_sabor: int = sa.Column(sa.Integer, sa.ForeignKey("sabores.id"))
    sabor: Mapped["Sabor"] = orm.relationship("Sabor", lazy="joined")

    id_tipo_embalagem: int = sa.Column(sa.Integer, sa.ForeignKey("tipos_embalagem.id"))
    tipo_embalagem: Mapped["TipoEmbalagem"] = orm.relationship(
        "TipoEmbalagem", lazy="joined"
    )

    id_tipo_picole: int = sa.Column(sa.Integer, sa.ForeignKey("tipos_picole.id"))
    tipo_picole: Mapped["TipoPicole"] = orm.relationship("TipoPicole", lazy="joined")

    # Um picole pode ter vários ingredientes
    ingredientes: Mapped[List["Ingrediente"]] = orm.relationship(
        "Ingrediente",
        secondary=ingredientes_picole,
        backref="ingrediente",
        lazy="joined",
    )

    # Um picolé pode ter vários conservantes ou mesmo nenhum
    conservantes: Mapped[List["Conservante"]] = orm.relationship(
        "Conservante",
        secondary=conservantes_picole,
        backref="conservante",
        lazy="joined",
    )

    # Um picole pode ter vários aditivos nutritivos ou mesmo nenhum
    aditivos_nutritivos: Mapped[List["AditivoNutritivo"]] = orm.relationship(
        "AditivoNutritivo",
        secondary=aditivos_nutritivos_picole,
        backref="aditivo_nutritivo",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return (
            f"Picole("
            f"id={self.id}, "
            f"data_criacao={self.data_criacao}, "
            f"preco={self.preco}, "
            f"id_sabor={self.id_sabor}, "
            f"id_tipo_embalagem={self.id_tipo_embalagem}, "
            f"id_tipo_picole={self.id_tipo_picole}, "
            f")"
        )
