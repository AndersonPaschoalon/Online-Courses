package br.com.alura.alugames.modelo
import java.time.LocalDate
import java.time.Period

class Periodo (val dataInicial: LocalDate,
               val dataFinal: LocalDate) {
    val emDias = Period.between(dataInicial, dataFinal).days
}