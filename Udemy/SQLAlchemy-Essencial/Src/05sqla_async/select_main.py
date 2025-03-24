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


def select_filtro_sabor(id_sabor: int, forma=1) -> None:
    with create_session(use_sqlite) as session:
        if forma == 1:
            # Forma 1
            sabor: Sabor = session.query(Sabor).filter(Sabor.id == id_sabor).first()
            print(sabor)
        if forma == 2:
            # forma 2
            sabor: Sabor = (
                session.query(Sabor).filter(Sabor.id == id_sabor).one_or_none()
            )
            print(sabor)
        if forma == 3:
            # forma 3
            sabor: Sabor = session.query(Sabor).filter(Sabor.id == id_sabor).one()
            print(sabor)
        if forma == 4:
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


def select_group_by_picole() -> None:
    with create_session(use_sqlite) as session:
        picoles: List[Picole] = (
            session.query(Picole).group_by(Picole.id, Picole.id_tipo_picole).all()
        )
        for picole in picoles:
            print(picole)
            print(picole.tipo_picole)
            print(picole.sabor)


def select_limit() -> None:
    with create_session(use_sqlite) as session:
        sabores: List[Sabor] = session.query(Sabor).limit(25)
        for sabor in sabores:
            print(sabor)


def select_count_revendedor() -> None:
    with create_session(use_sqlite) as session:
        q: int = session.query(Revendedor).count()
        print(f"Quantidade de revendedores: {q}")


def select_agragacao() -> None:
    with create_session(use_sqlite) as session:
        resultado: List = session.query(
            func.sum(Picole.preco).label("soma"),
            func.avg(Picole.preco).label("media"),
            func.min(Picole.preco).label("mais_barato"),
            func.max(Picole.preco).label("mais_caro"),
        ).all()

        print(f"Soma:{resultado[0][0]}")
        print(f"Média:{resultado[0][1]}")
        print(f"Mais Barato:{resultado[0][2]}")
        print(f"Mais Caro:{resultado[0][3]}")


if __name__ == "__main__":
    # select_todos_aditivos_nutritivos()
    # select_filtro_sabor(1)
    # select_complexo_picole()
    # select_order_by_sabor()
    # select_group_by_picole()
    # select_limit()
    # select_count_revendedor()
    select_agragacao()
