package br.com.alura.alugames.modelo

import java.time.LocalDate
import java.util.Scanner
import kotlin.random.Random

data class Gamer(var nome: String, var email: String): Recomendavel {
    var dataNascimento: String? = null
    var usuario: String? = null
        set(value){
            field = value
            if (idInterno.isNullOrBlank())
            {
                criarIdInterno()
            }
        }
    var idInterno: String? = null
        private set

    var plano: Plano = PlanoAvulso("BRONZE")

    val jobosBuscados = mutableListOf<Jogo?>()

    val jogosAlugados = mutableListOf<Aluguel>()

    private val listaNotas = mutableListOf<Int>()

    val jogosRecomendados = mutableListOf<Jogo>()

    override val media: Double
        get() = listaNotas.average()

    override fun recomendar(nota: Int) {
        listaNotas.add(nota)
    }

    fun recomendarJogo(jogo: Jogo, nota: Int){
        jogo.recomendar(nota)
        jogosRecomendados.add(jogo)

    }

    constructor(nome: String, email: String, dataNascimento: String, usuario: String):
            this(nome, email){
                this.dataNascimento = dataNascimento
                this.usuario = usuario
            }

    init {
        if(nome.isNullOrBlank()) {
             throw IllegalArgumentException("Nome está em branco.")
        }
        this.email = validarEmail()
    }

    override fun toString(): String {
        return "Gamer(nome='$nome', email='$email', dataNascimento=$dataNascimento, usuario=$usuario, idInterno=$idInterno, Reputação: $media)\n"
    }

    private fun criarIdInterno(){
        val numero = Random.nextInt(10000)
        val tag = String.format("%04d", numero)
        this.idInterno = "$usuario#$tag"
    }

    fun alugaJogo(jogo: Jogo, periodo: Periodo): Aluguel{
        val aluguel = Aluguel(this, jogo, periodo)
        jogosAlugados.add(aluguel)
        return aluguel
    }

    fun validarEmail(): String{
        val regex = Regex("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\$")
        if(regex.matches(email)){
            return email
        } else{
            throw  IllegalArgumentException("Email invalido")
        }
    }

    fun jogosDoMes(mes:Int): List<Jogo> {
        return jogosAlugados
            .filter { aluguel ->  aluguel.periodo.dataInicial.monthValue == mes}
            .map { aluguel ->  aluguel.jogo}
    }


    companion object{
        fun criarGamer(leitura: Scanner): Gamer{
            println("Boas vindas ao AliGames! Vamos fazer seu cadastro.")
            println("Nome:")
            val nome = leitura.nextLine()
            println("Email:")
            val email = leitura.nextLine()
            println("Deseja completar o cadastro com usuario e data de nascimento (S/N)")
            val opcao = leitura.nextLine()

            if (opcao.equals("s", true)) {
                println("Data de nascimento (DD/MM/AAAA):")
                val nascimento = leitura.nextLine()
                println("Usuario:")
                val usuario = leitura.nextLine()

                return Gamer(nome, email, nascimento, usuario)
            }
            else {
                return Gamer(nome, email)
            }

        }
    }

}
