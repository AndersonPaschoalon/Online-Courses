from conf.db_session import create_session
from models.picole import Picole
from models.sabor import Sabor

use_sqlite = True


def select_filtro_picole(id_picole: int) -> None:
    with create_session(use_sqlite=use_sqlite) as session:
        picole: Picole = (
            session.query(Picole).where(Picole.id == id_picole).one_or_none()
        )
        print(picole)
        print(f"\t{picole.sabor}")
        print("----")


def atualizar_sabor(id_sabor: int, novo_nome: str) -> None:
    with create_session(use_sqlite=use_sqlite) as session:
        sabor: Sabor = session.query(Sabor).filter(Sabor.id == id_sabor).one_or_none()
        if sabor:
            sabor.nome = novo_nome
            session.commit()
        else:
            print(f"Não existe sabor com ID {id_sabor}")


def exemplo_update():
    from select_main import select_filtro_sabor

    id_sabor = 42
    select_filtro_sabor(id_sabor=id_sabor)
    atualizar_sabor(id_sabor=id_sabor, novo_nome="Banana")
    select_filtro_sabor(id_sabor=id_sabor)


def atualizar_picole(id_picole: int, novo_preco: float, novo_sabor: int = None):
    with create_session(use_sqlite=use_sqlite) as session:
        picole: Picole = (
            session.query(Picole).filter(Picole.id == id_picole).one_or_none()
        )
        if picole:
            picole.preco = novo_preco
            if novo_sabor:
                picole.id_sabor = novo_sabor
            session.commit()
        else:
            print(f"Não existe picole com id {id_picole}")


if __name__ == "__main__":
    # exemplo_update()
    id_picole = 21
    novo_preco = 9.99
    id_novo_sabor = 42
    select_filtro_picole(id_picole=id_picole)
    atualizar_picole(
        id_picole=id_picole, novo_preco=novo_preco, novo_sabor=id_novo_sabor
    )
    select_filtro_picole(id_picole=id_picole)
