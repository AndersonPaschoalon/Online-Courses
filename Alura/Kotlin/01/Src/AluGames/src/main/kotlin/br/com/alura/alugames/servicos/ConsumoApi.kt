package br.com.alura.alugames.servicos
import br.com.alura.alugames.modelo.InfoApiShark
import br.com.alura.alugames.modelo.InfoGamerJson
import br.com.alura.alugames.modelo.InfoJogo
import br.com.alura.alugames.modelo.InfoJogoJson
import br.com.alura.alugames.modelo.Gamer
import br.com.alura.alugames.modelo.Jogo
import br.com.alura.alugames.utilitario.criaGamer
import br.com.alura.alugames.utilitario.criaJogo
import com.google.gson.Gson
import java.net.URI
import java.lang.reflect.Type
import com.google.gson.reflect.TypeToken
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse.BodyHandlers


class ConsumoApi {

    private fun consomeDados(endereco: String): String{
        // https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpRequest.html
        val client: HttpClient = HttpClient.newHttpClient()
        val request = HttpRequest.newBuilder()
            .uri(URI.create(endereco))
            .build()

        val response = client
            .send(request, BodyHandlers.ofString())
        //  println("json: $json ")
        return response.body()
    }

    fun buscaJogo(id: String): InfoJogo
    {
        val endreco = "https://www.cheapshark.com/api/1.0/games?id=$id"
        val json = consomeDados(endereco = endreco)
        var meuInfoJogo: InfoJogo? = null

        // id falha   - 174
        // id sucesso - 150
        val resultado = runCatching {
            val gson = Gson()
            meuInfoJogo = gson.fromJson(json, InfoJogo::class.java)
            return meuInfoJogo!!
        }
        return InfoJogo(InfoApiShark("", ""))
    }


    fun buscaGamers(): List<Gamer>
    {

        val endereco = "https://raw.githubusercontent.com/jeniblodev/arquivosJson/main/gamers.json"
        val json = consomeDados(endereco)

        val gson = Gson()
        val meuGamerTipo = object: TypeToken<List<InfoGamerJson>>(){}.type
        val listaGamer: List<InfoGamerJson> = gson.fromJson(json, meuGamerTipo)

        val listaGamerMap = listaGamer.map{ infoGamerJson -> infoGamerJson.criaGamer() }

        return listaGamerMap

    }

    fun buscaJogosJson(): List<Jogo> {
        val endereco = "https://raw.githubusercontent.com/jeniblodev/arquivosJson/main/jogos.json"
        val json = consomeDados(endereco)

        val gson = Gson()
        val meuJogoTipo = object : TypeToken<List<InfoJogoJson>>() {}.type
        val listaJogo: List<InfoJogoJson> = gson.fromJson(json, meuJogoTipo)

        val listaJogoConvertida = listaJogo.map { infoJogoJson -> infoJogoJson.criaJogo() }

        return listaJogoConvertida
    }

}