package br.com.alura.alugames.principal
import br.com.alura.alugames.modelo.Gamer
import br.com.alura.alugames.modelo.Jogo
import br.com.alura.alugames.servicos.ConsumoApi
import transformarEmIdade
import java.util.*
import java.nio.file.Paths

fun main() {

    println("Working dir:" + Paths.get("").toAbsolutePath().toString() )

    val leitura = Scanner(System.`in`)
    val gamer = Gamer.criarGamer(leitura)
    println("Cadastro concluido com sucesso. Dados do gamer:")
    println(gamer)
    println("Idate do gamer: " + gamer.dataNascimento?.transformarEmIdade())

    do {

        println("Digite o codigo de jogo para buscar:")
        val busca = leitura.nextLine()

        val buscaApi = ConsumoApi()
        val infoJogo = buscaApi.buscaJogo(busca)

        var meuJogo: Jogo? = null

        // id falha   - 174
        // id sucesso - 150
        val resultado = runCatching {

            meuJogo = Jogo(
                infoJogo.info.title,
                infoJogo.info.thumb
            )
        }

        resultado.onFailure {
            println("br.com.alura.alugames.modelo.Jogo inexistente, tente outro id!")
        }

        resultado.onSuccess {
            println("Deseja inserir uma descrição personalizada? s/n")
            val opcao = leitura.nextLine()
            if (opcao.equals("s", ignoreCase = true)) {
                println("Insira a descrição personalizada para o jogo:")
                val descricaoPersonalizada = leitura.nextLine()
                meuJogo?.descricao = descricaoPersonalizada
            } else {
                meuJogo?.descricao = meuJogo?.titulo
            }

            gamer.jobosBuscados.add(meuJogo)
        }

        println("Deseja buscar um novo jogo? S/N")
        var resposta = leitura.nextLine()


    }while (resposta.equals("s", ignoreCase = true))

    println("Jogos Buscados:")
    println(gamer.jobosBuscados)

    println("Jogos ordenados por titulo")
    gamer.jobosBuscados.sortBy {
        it?.titulo
    }

    gamer.jobosBuscados.forEach{
        println("Titulo:" + it?.titulo)
    }

    val jogosFiltrados = gamer.jobosBuscados.filter {
        it?.titulo?.contains("batman", true) ?: false
    }
    println("Jogos filtrados (batman):")
    println(jogosFiltrados)

    println("Deseja excluir algum jogo da lista original? S/N")
    val opcao = leitura.nextLine()
    if(opcao.equals("s", true)){
        println(gamer.jobosBuscados)
        println("\nInforme a posiçaao do jogo que deseja excluir:")
        val posicao = leitura.nextInt()
        gamer.jobosBuscados.removeAt(posicao)
    }

    println("\nLista Atualizada")
    println(gamer.jobosBuscados)


    println("Busca finalizada com sucesso.")

}