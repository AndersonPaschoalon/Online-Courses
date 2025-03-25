import asyncio

from conf.db_session import create_session
from models.aditivo_nutritivo import AditivoNutritivo
from models.conservante import Conservante
from models.ingrediente import Ingrediente
from models.join_tables import (
    aditivos_nutritivos_picole,
    conservantes_picole,
    ingredientes_picole,
    lotes_nota_fiscal,
)
from models.lote import Lote
from models.nota_fiscal import NotaFiscal
from models.picole import Picole
from models.revendedor import Revendedor
from models.sabor import Sabor
from models.tipo_embalagem import TipoEmbalagem
from models.tipo_picole import TipoPicole

# use_sqlite = True

use_sqlite = False


async def insert_aditivo_nutritivo() -> AditivoNutritivo:
    print("Cadastro Aditivo Nutritivo")

    nome: str = input("Informe o nome do Aditivo Nutritivo: ")
    formula_quimica: str = input("Informe a fórmula quimica do aditivo: ")

    an: AditivoNutritivo = AditivoNutritivo(nome=nome, formula_quimica=formula_quimica)

    async with create_session(use_sqlite) as session:
        session.add(an)
        await session.commit()

    print("Aditivo Nutritivo cadastrado com sucesso")
    print(f"{an}")
    return an


async def insert_sabor() -> Sabor:
    print("Cadastrando Sabor")

    nome: str = input("Informe o nome do sabor: ")

    sabor: Sabor = Sabor(nome=nome)

    async with create_session(use_sqlite) as session:
        session.add(sabor)
        await session.commit()

    print("Sabor cadastrado com sucesso")
    print(sabor)
    return sabor


async def insert_tipo_embalagem() -> TipoEmbalagem:
    print("Cadastrando Tipo Embalagem")

    nome: str = input("Informe o nome do Tipo Embalagem: ")

    te: TipoEmbalagem = TipoEmbalagem(nome=nome)

    async with create_session(use_sqlite) as session:
        session.add(te)
        await session.commit()

    print("Tipo Embalagem cadastrado com sucesso")
    print(te)
    return te


async def insert_tipo_picole() -> TipoPicole:
    print("Cadastrando Tipo Picole")

    nome: str = input("Informe o nome do Tipo Picole: ")

    tp: TipoPicole = TipoPicole(nome=nome)

    async with create_session(use_sqlite) as session:
        session.add(tp)
        await session.commit()

    print("Tipo Picole cadastrado com sucesso")
    print(tp)
    return tp


async def insert_ingrediente() -> Ingrediente:
    print("Cadastrando Ingrediente")

    nome: str = input("Informe o nome do Ingrediente: ")
    ing: Ingrediente = Ingrediente(nome=nome)

    async with create_session(use_sqlite) as session:
        session.add(ing)
        await session.commit()

    print("Ingrediente cadastrado com sucesso")
    print(ing)
    return ing


async def insert_conservante() -> Conservante:
    print("Cadastrando Conservante")

    nome: str = input("Informe o nome do Conservante: ")
    descricao: str = input("Informe a descrição do Conservante: ")
    conservante: Conservante = Conservante(nome=nome, descricao=descricao)

    async with create_session(use_sqlite) as session:
        session.add(conservante)
        await session.commit()

    print("Conservante cadastrado com sucesso")
    print(conservante)
    return conservante


async def insert_revendedor() -> Revendedor:
    print("Cadastrando Revendedor")

    cnpj: str = input("Informe o CNPJ do Revendedor: ")
    razao_social: str = input("Informe a Razão Social do Revendedor: ")
    contato: str = input("Informe Contato do Revendedor: ")
    rev: Revendedor = Revendedor(cnpj=cnpj, razao_social=razao_social, contato=contato)

    async with create_session(use_sqlite) as session:
        session.add(rev)
        await session.commit()

    print("Revendedor cadastrado com sucesso")
    print(rev)
    return rev


async def insert_lote() -> Lote:
    print("Cadastrando Revendedor")

    id_tipo_picole: str = input("Informe o ID do tipo de Picole: ")
    quantidade: int = input("Informe a Quantidade: ")
    lt = Lote(id_tipo_picole=id_tipo_picole, quantidade=quantidade)

    async with create_session(use_sqlite) as session:
        session.add(lt)
        await session.commit()

    print("Lote cadastrado com sucesso")
    print(lt)
    return lt


async def insert_nota_fical() -> NotaFiscal:
    print("Cadastrando Nota Fiscal")

    valor: float = input("Informe o valor da nota fiscal: ")
    numero_serie: str = input("Informe o número de série: ")
    descricao: str = input("Informe a descrição: ")
    id_revendedor = input("Informe o ID do Revendedor: ")

    nf: NotaFiscal = NotaFiscal(
        valor=valor,
        numero_serie=numero_serie,
        descricao=descricao,
        id_revendedor=id_revendedor,
    )

    n_lotes = int(input("Informar numero de lotes a serem criados"))

    for i in range(n_lotes):
        print(f"Inserir Lote {i}: ")
        print("----")
        lote1 = insert_lote()
        nf.lotes.append(lote1)

    async with create_session(use_sqlite) as session:
        session.add(nf)
        await session.commit()

    print("Nota Fiscal cadastrada com sucesso")
    print(nf)
    return NotaFiscal


async def insert_picole() -> Picole:
    print("Cadastrando Picole")

    preco: float = input("Informe o preço do picole: ")
    id_sabor: int = input("Informe o ID do sabor: ")
    id_tipo_picole: int = input("Informe o ID do tipo de picole: ")
    id_tipo_embalagem: int = input("Informe o ID do tipo da embalagem: ")

    picole: Picole = Picole(
        id_sabor=id_sabor,
        id_tipo_embalagem=id_tipo_embalagem,
        id_tipo_picole=id_tipo_picole,
        preco=preco,
    )

    n_ingredientes: int = int(input("Numero de ingredientes:"))
    for i in range(n_ingredientes):
        id_ingrediente: int = input(f"Id do ingrediente {i}: ")
        async with create_session(use_sqlite) as session:
            ing = session.get(Ingrediente, id_ingrediente)
            print(ing)
            picole.ingredientes.append(ing)

    n_con: int = int(input("Numero de conservantes:"))
    for i in range(n_con):
        id_con: int = input(f"Id do conservante {i}: ")
        async with create_session(use_sqlite) as session:
            c = session.get(Conservante, id_con)
            print(c)
            picole.conservantes.append(c)

    n_add: int = int(input("Numero de aditivos nutritivos:"))
    for i in range(n_add):
        id_con: int = input(f"Id do conservante {i}: ")
        async with create_session(use_sqlite) as session:
            a = session.get(AditivoNutritivo, id_con)
            print(a)
            picole.aditivos_nutritivos.append(a)

    async with create_session(use_sqlite) as session:
        session.add(picole)
        await session.commit()
        print("Picole cadastrado com sucesso")

    print(picole)
    return Picole


def main():
    while True:
        print("\nMenu de Cadastro:")
        print("(01) Aditivo Nutritivo")
        print("(02) Sabor")
        print("(03) Tipo de Embalagem")
        print("(04) Tipo de Picolé")
        print("(05) Ingrediente")
        print("(06) Conservante")
        print("(07) Revendedor")
        print("(08) Lote (requer ID do tipo de picole)")
        print("(09) Nota Fiscal(Requer ID do revendedor)")
        print(
            "(10) Picole (requer ID de sabor, tipo de picole, tipo de embalagem e IDS de ingredientes, conservantes e aditivos nutritivos se houverem)"
        )
        print("(99) Sair\n")

        opt: int = int(input("Escolha uma opção: "))

        if opt == 1:
            asyncio.run(insert_aditivo_nutritivo())
        elif opt == 2:
            asyncio.run(insert_sabor())
        elif opt == 3:
            asyncio.run(insert_tipo_embalagem())
        elif opt == 4:
            asyncio.run(insert_tipo_picole())
        elif opt == 5:
            asyncio.run(insert_ingrediente())
        elif opt == 6:
            asyncio.run(insert_conservante())
        elif opt == 7:
            asyncio.run(insert_revendedor())
        elif opt == 8:
            asyncio.run(insert_lote())
        elif opt == 9:
            asyncio.run(insert_nota_fical())
        elif opt == 10:
            asyncio.run(insert_picole())
        elif opt == 99:
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()


"""
aditivos_nutritivos
    "nome": "Vitamina C", "formula_quimica": "C6H8O6"
    "nome": "Ferro", "formula_quimica": "Fe"

sabores
    "Morango", "Chocolate", "Baunilha"

tipos_embalagem
    "Plástico", "Papel", "Metal"

tipos_picole
    "Frutado", "Cremoso", "Diet"

ingredientes
"Leite", "Açúcar", "Cacau", "Frutas Vermelhas"

conservantes
    {"nome": "Ácido Sórbico", "descricao": "Conservante natural."
    {"nome": "Benzoato de Sódio", "descricao": "Evita mofo e fungos."

revendedores
    "cnpj": "12.345.678/0001-99", "razao_social": "Sorvetes do Brasil", "contato": "(11) 99999-9999"
    "cnpj": "98.765.432/0001-11", "razao_social": "Gela Tudo", "contato": "(21) 88888-8888"

"""
