package br.com.andersonp.orgs.ui.activity

import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.RecyclerView
import br.com.andersonp.orgs.R
import br.com.andersonp.orgs.dao.ProdutosDao
import br.com.andersonp.orgs.ui.recyclerview.adapter.ListaProdutosAdapter
import com.google.android.material.floatingactionbutton.FloatingActionButton

class ListaProdutosActivity : AppCompatActivity(R.layout.activity_lista_produtos) {

    private val dao = ProdutosDao()
    private val adapter = ListaProdutosAdapter(context = this, produtos = this.dao.buscaTodos())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        configuraRecyclerView()

    }

    override fun onResume() {
        super.onResume()
        this.adapter.atualiza(this.dao.buscaTodos())
        Log.i("MainActivity", "onCreate: ${this.dao.buscaTodos()}")
        configuraFab()
    }

    private fun configuraFab() {
        val fab = findViewById<FloatingActionButton>(R.id.activity_lista_produtos_fab)
        fab.setOnClickListener {
            val intent = Intent(this, FormularioProdutoActivity::class.java)
            startActivity(intent)
        }
    }

    private fun configuraRecyclerView() {
        val recyclerView = findViewById<RecyclerView>(R.id.activity_lista_produtos_recyclerView)
        recyclerView.adapter = this.adapter
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