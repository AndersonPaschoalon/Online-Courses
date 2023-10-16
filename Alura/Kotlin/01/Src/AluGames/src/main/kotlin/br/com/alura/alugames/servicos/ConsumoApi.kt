package br.com.alura.alugames.servicos
import br.com.alura.alugames.modelo.InfoApiShark
import br.com.alura.alugames.modelo.InfoJogo
import com.google.gson.Gson
import java.net.URI
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse.BodyHandlers


class ConsumoApi {

    fun buscaJogo(id: String): InfoJogo
    {
        val endreco = "https://www.cheapshark.com/api/1.0/games?id=$id"

        println("*********************************************")
        // https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpRequest.html
        val client: HttpClient = HttpClient.newHttpClient()
        val request = HttpRequest.newBuilder()
            .uri(URI.create(endreco))
            .build()

        val response = client
            .send(request, BodyHandlers.ofString())
        val json = response.body()
        println("json: $json ")

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
}