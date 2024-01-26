package br.com.andersonp.orgs.ui.activity

import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.compose.material3.AlertDialog
import androidx.recyclerview.widget.RecyclerView
import br.com.andersonp.orgs.R
import br.com.andersonp.orgs.dao.ProdutosDao
import br.com.andersonp.orgs.databinding.ActivityListaProdutosBinding
import br.com.andersonp.orgs.ui.recyclerview.adapter.ListaProdutosAdapter
import com.google.android.material.floatingactionbutton.FloatingActionButton



class ListaProdutosActivity : AppCompatActivity() {

    private val dao = ProdutosDao()
    private val adapter = ListaProdutosAdapter(context = this, produtos = this.dao.buscaTodos())
    private val binding by lazy {
        ActivityListaProdutosBinding.inflate(this.layoutInflater)
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        this.setContentView(this.binding.root)
        this.configuraRecyclerView()
        this.configuraFab()
    }

    override fun onResume() {
        super.onResume()

        this.adapter.atualiza(this.dao.buscaTodos())
        Log.i("MainActivity", "onCreate: ${this.dao.buscaTodos()}")
    }

    private fun configuraFab() {
        val fab = this.binding.activityListaProdutosFab
        fab.setOnClickListener{
            val intent = Intent(this, FormularioProdutoActivity::class.java)
            this.startActivity(intent)
        }
    }

    private fun configuraRecyclerView() {
        val recyclerView = this.binding.activityListaProdutosRecyclerView
        recyclerView.adapter = this.adapter
    }


}

