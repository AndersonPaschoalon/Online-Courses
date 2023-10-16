package br.com.alura.alugames.principal
import br.com.alura.alugames.modelo.Gamer

fun main(){
    val gamer1 = Gamer("Joao", "joao@gmai.com")
    println(gamer1)
    gamer1.let{
        it.dataNascimento = "01/01/1900"
        it.usuario = "Pedro"
    }.also {
        println(gamer1.idInterno)
    }

    println(gamer1)
    gamer1.usuario = "Joao"

    println(gamer1.usuario)
}
