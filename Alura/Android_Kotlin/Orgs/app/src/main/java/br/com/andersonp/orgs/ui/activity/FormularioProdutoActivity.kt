package br.com.andersonp.orgs.ui.activity
// https://developer.android.com/jetpack/androidx?hl=pt-br
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import br.com.andersonp.orgs.R
import br.com.andersonp.orgs.dao.ProdutosDao
import br.com.andersonp.orgs.model.Produto
import java.math.BigDecimal

class FormularioProdutoActivity : AppCompatActivity(R.layout.activity_formulario_produto) {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val  botaoSalvar = findViewById<Button>(R.id.activity_formulario_botao_salvar)
        botaoSalvar.setOnClickListener {
            val novoProduto = this.criaProduto()
            val dao = ProdutosDao()
            dao.adiciona(novoProduto)
            Log.d("FormularioProduto", "***************  ${dao.buscaTodos()}")
            finish()
        }
    }

    private fun criaProduto(): Produto
    {
        val nome = findViewById<EditText>(R.id.activity_formulario_nome).text.toString()
        val descricao = findViewById<EditText>(R.id.activity_formulario_descricao).text.toString()
        val valorTxt = findViewById<EditText>(R.id.activity_formulario_valor).text.toString()
        val valor = if(valorTxt.isBlank()){
            BigDecimal.ZERO
        } else {
            BigDecimal(valorTxt)
        }

        val novoProduto = Produto(
            nome=nome,
            descricao=descricao,
            valor = valor)
        Log.d("FormularioProduto", "*************** novoProduto $novoProduto")

        return novoProduto
    }
}


/*
Old implementation
class FormularioProdutoActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_formulario_produto)
    }
}
*/