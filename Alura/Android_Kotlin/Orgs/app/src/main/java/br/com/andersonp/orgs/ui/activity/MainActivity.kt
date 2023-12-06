package br.com.andersonp.orgs.ui.activity

import android.app.Activity

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import br.com.andersonp.orgs.R
import br.com.andersonp.orgs.model.Produto
import br.com.andersonp.orgs.ui.recyclerview.adapter.ListaProdutosAdapter
import java.math.BigDecimal

class MainActivity : AppCompatActivity(R.layout.activity_main) {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val recyclerView = findViewById<RecyclerView>(R.id.recyclerView)
        recyclerView.adapter = ListaProdutosAdapter(
            context = this, produtos = listOf(
                Produto(nome = "test01", descricao = "descricao 01", valor = BigDecimal("19.99")),
                Produto(nome = "test02", descricao = "descricao 02", valor = BigDecimal("10.99")),
                Produto(nome = "test03", descricao = "descricao 03", valor = BigDecimal("1.99")),
                Produto(nome = "test04", descricao = "descricao 04", valor = BigDecimal("0.01")),
            )
        )
    }

}

/*
class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val recyclerView = findViewById<RecyclerView>(R.id.recyclerView)
        recyclerView.adapter = ListaProdutosAdapter(
            context = this, produtos = listOf(
                Produto(nome = "test01", descricao = "descricao 01", valor = BigDecimal("19.99")),
                Produto(nome = "test02", descricao = "descricao 02", valor = BigDecimal("10.99")),
                Produto(nome = "test03", descricao = "descricao 03", valor = BigDecimal("1.99")),
                Produto(nome = "test04", descricao = "descricao 04", valor = BigDecimal("0.01")),
            )
        )
    }

}

*/