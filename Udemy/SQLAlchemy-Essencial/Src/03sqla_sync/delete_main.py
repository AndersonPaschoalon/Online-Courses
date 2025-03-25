from typing import Optional

from conf.db_session import create_session
from models.picole import Picole
from models.revendedor import Revendedor

use_sqlite = True


def deletar_picole(id_picole: int) -> None:
    with create_session(use_sqlite=use_sqlite) as session:
        picole: Optional[Picole] = (
            session.query(Picole).filter(Picole.id == id_picole).one_or_none()
        )
        if picole:
            session.delete(picole)
            session.commit()
        else:
            print(f"Não foi posível encontrar picole com id {id_picole}")


def test_delete_picole():
    from update_main import select_filtro_picole

    id_picole = 21
    select_filtro_picole(id_picole=id_picole)
    deletar_picole(id_picole=id_picole)
    select_filtro_picole(id_picole=id_picole)


def select_filtro_revendedor(id_revendedor: int) -> None:
    with create_session(use_sqlite=use_sqlite) as session:
        revendedor: Optional[Revendedor] = session.query(Revendedor).filter(Revendedor.id == id_revendedor)

        if revendedor: 
            print(f"revendedor: {revendedor}")
        else:
            print(f"Não encontrei nenhum revendedor com id {id_revendedor}")

def deletar_revendedor(id_revendedor: int) -> None:
    with create_session(use_sqlite=use_sqlite) as session:
        revendedor: Optional[Revendedor] = session.query(Revendedor).filter(Revendedor.id == id_revendedor)

        if revendedor: 
            print(f"revendedor: {revendedor}")
            session.delete(revendedor)
            session.commit()
            print(f"revendedor deletado!")
        else:
            print(f"Não encontrei nenhum revendedor com id {id_revendedor}")




if __name__ == "__main__":
    # test_delete_picole()
