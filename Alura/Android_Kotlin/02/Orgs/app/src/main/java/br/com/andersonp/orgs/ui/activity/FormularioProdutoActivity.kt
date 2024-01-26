package br.com.andersonp.orgs.ui.activity
// https://developer.android.com/jetpack/androidx?hl=pt-br
import android.os.Build.VERSION.SDK_INT
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import br.com.andersonp.orgs.R
import br.com.andersonp.orgs.dao.ProdutosDao
import br.com.andersonp.orgs.databinding.ActivityFormularioProdutoBinding
import br.com.andersonp.orgs.databinding.FormularioImagemBinding
import br.com.andersonp.orgs.extensions.tryToLoad
import br.com.andersonp.orgs.model.Produto
// import coil.ImageLoader
// import coil.decode.GifDecoder
// import coil.decode.ImageDecoderDecoder
import coil.load
import java.math.BigDecimal

class FormularioProdutoActivity : AppCompatActivity() {

    private val binding by lazy {
        ActivityFormularioProdutoBinding.inflate(this.layoutInflater)
    }

    private var url : String? = null


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
        title = "Cadastrar Produto"
        val  botaoSalvar = this.binding.activityFormularioBotaoSalvar
        val dao = ProdutosDao()
        botaoSalvar.setOnClickListener{
            val novoProduto = this.criaProduto()
            dao.adiciona(novoProduto)
            Log.d("FormularioProduto", "***************  ${dao.buscaTodos()}")
            finish()
        }

        binding.activityFormularioProdutoImagem.setOnClickListener{
            val bindingFormularioImagem = FormularioImagemBinding.inflate(layoutInflater)
            bindingFormularioImagem.formularioImagemBotaoCarregar.setOnClickListener{
                this.url = bindingFormularioImagem.formularioImagemUrl.text.toString()
                bindingFormularioImagem.formularioImagemImageview.tryToLoad(this.url)
            }


            AlertDialog.Builder(this)
                .setView(bindingFormularioImagem.root)
                .setPositiveButton("Confirmar") { _, _ ->
                    val url = bindingFormularioImagem.formularioImagemUrl.text.toString()

                    binding.activityFormularioProdutoImagem.tryToLoad(this.url)

                }
                .setNegativeButton("Cancelar") { _, _ ->

                }
                .show()

        }
    }
    /*
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
     */

    private fun criaProduto(): Produto
    {
        //val nome = findViewById<EditText>(R.id.activity_formulario_nome).text.toString()
        val nome = this.binding.activityFormularioNome.text.toString()

        //val descricao = findViewById<EditText>(R.id.activity_formulario_descricao).text.toString()
        val descricao = this.binding.activityFormularioDescricao.text.toString()

        // val valorTxt = findViewById<EditText>(R.id.activity_formulario_valor).text.toString()
        val valorTxt = this.binding.activityFormularioValor.text.toString()

        val valor = if(valorTxt.isBlank()){
            BigDecimal.ZERO
        } else {
            BigDecimal(valorTxt)
        }

        val novoProduto = Produto(
            nome=nome,
            descricao=descricao,
            valor = valor,
            imagem = url
        )
        Log.d("FormularioProduto", "*************** novoProduto $novoProduto")

        return novoProduto
    }
}


