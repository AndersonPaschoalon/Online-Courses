import sqlalchemy as sa

from models.model_base import ModelBase

# Nota Fiscal pode ter vários lotes
lotes_nota_fiscal = sa.Table(
    "lotes_nota_fiscal",
    ModelBase.metadata,
    sa.Column("id_nota_fiscal", sa.Integer, sa.ForeignKey("notas_fiscais.id")),
    sa.Column("id_lote", sa.Integer, sa.ForeignKey("lotes.id")),
)

# Picolé pode ter vários ingredientes
ingredientes_picole = sa.Table(
    "ingredientes_picole",
    ModelBase.metadata,
    sa.Column("id_picole", sa.Integer, sa.ForeignKey("picoles.id")),
    sa.Column("id_ingrediente", sa.Integer, sa.ForeignKey("ingredientes.id")),
)

# Picolé pode ter vários conservantes
conservantes_picole = sa.Table(
    "conservantes_picole",
    ModelBase.metadata,
    sa.Column("id_picole", sa.Integer, sa.ForeignKey("picoles.id")),
    sa.Column("id_conservante", sa.Integer, sa.ForeignKey("conservantes.id")),
)

# Picole pode ter vários aditivos nutritivos
aditivos_nutritivos_picole = sa.Table(
    "aditivos_nutritivos_picole",
    ModelBase.metadata,
    sa.Column("id_picole", sa.Integer, sa.ForeignKey("picoles.id")),
    sa.Column(
        "id_aditivo_nutritivo", sa.Integer, sa.ForeignKey("aditivos_nutritivos.id")
    ),
)
