package br.com.andersonp.orgs.dao

import br.com.andersonp.orgs.model.Produto
import java.math.BigDecimal

class ProdutosDao {

    fun adiciona(produto: Produto) {
        Companion.produtos.add(produto)
    }

    fun buscaTodos(): List<Produto> {
        return Companion.produtos.toList()
    }

    companion object {
        // private val produtos = mutableListOf<Produto>()
        private val produtos = mutableListOf<Produto>(
            Produto(
                nome = "Salada de Frutas",
                descricao = "Laranja, Maçãns e Uva",
                valor = BigDecimal("19.83")
            )
        )
    }
}