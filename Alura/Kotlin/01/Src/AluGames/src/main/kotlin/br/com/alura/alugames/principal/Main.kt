package br.com.alura.alugames.principal
import br.com.alura.alugames.modelo.Jogo
import br.com.alura.alugames.servicos.ConsumoApi
import java.util.*


fun main() {

    val leitura = Scanner(System.`in`)

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
            println("meuJogo: $meuJogo")
        }

        println("Deseja buscar um novo jogo? S/N")
        var resposta = leitura.nextLine()


    }while (resposta.equals("s", ignoreCase = true))

    println("Busca finalizada com sucesso.")

}