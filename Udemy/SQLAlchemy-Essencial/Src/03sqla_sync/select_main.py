from typing import List

from sqlalchemy import func

from conf.db_session import create_session
from conf.helpers import formata_data
from models.aditivo_nutritivo import AditivoNutritivo
from models.picole import Picole
from models.revendedor import Revendedor
from models.sabor import Sabor

use_sqlite = True


## SELECT * FROM aditivos_nutritivos
def select_todos_aditivos_nutritivos() -> None:
    with create_session(use_sqlite) as session:

        # Froma 1
        aditivos_nutritivos: List[AditivoNutritivo] = session.query(AditivoNutritivo)
        for an in aditivos_nutritivos:
            print(an)

        # forma 2
        aditivos_nutritivos: List[AditivoNutritivo] = session.query(
            AditivoNutritivo
        ).all()
        for an in aditivos_nutritivos:
            print(an)


def select_filtro_sabor(id_sabor: int) -> None:
    with create_session(use_sqlite) as session:
        # Forma 1
        sabor: Sabor = session.query(Sabor).filter(Sabor.id == id_sabor).first()
        print(sabor)
        # forma 2
        sabor: Sabor = session.query(Sabor).filter(Sabor.id == id_sabor).one_or_none()
        print(sabor)
        # forma 3
        sabor: Sabor = session.query(Sabor).filter(Sabor.id == id_sabor).one()
        print(sabor)
        # forma 4
        sabor: Sabor = session.query(Sabor).where(Sabor.id == id_sabor).one()
        print(sabor)


def select_complexo_picole() -> None:
    with create_session(use_sqlite) as session:
        picoles: List[Picole] = session.query(Picole).all()
        for picole in picoles:
            print(f"picole:{picole}")
            print(f"picole.sabor:{picole.sabor}")


def select_order_by_sabor() -> None:
    with create_session(use_sqlite) as session:
        sabores: List[Sabor] = (
            session.query(Sabor).order_by(Sabor.data_criacao.desc()).all()
        )
        for sabor in sabores:
            print(sabor)


if __name__ == "__main__":
    # select_todos_aditivos_nutritivos()
    # select_filtro_sabor(1)
    # select_complexo_picole()
    select_order_by_sabor()
