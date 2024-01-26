package br.com.andersonp.orgs.ui.recyclerview.adapter

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import br.com.andersonp.orgs.R
import br.com.andersonp.orgs.databinding.ProdutoItemBinding
import br.com.andersonp.orgs.extensions.tryToLoad
import br.com.andersonp.orgs.model.Produto
import coil.load
import java.text.NumberFormat
import java.util.Locale

class ListaProdutosAdapter(
    private val context: Context,
    produtos: List<Produto>
) : RecyclerView.Adapter<ListaProdutosAdapter.ViewHolder>() {

    private val produtos = produtos.toMutableList()

    class ViewHolder(private val binding: ProdutoItemBinding): RecyclerView.ViewHolder(binding.root) {

        fun vincula(produto: Produto) {
            // val nome =  itemView.findViewById<TextView>(R.id.produto_item_nome)
            val nome =  this.binding.produtoItemNome
            nome.text = produto.nome

            // val descricao =  itemView.findViewById<TextView>(R.id.produto_item_descricao)
            val descricao = this.binding.produtoItemDescricao
            descricao.text = produto.descricao

            // val valor =  itemView.findViewById<TextView>(R.id.produto_item_valor)
            val valor = this.binding.produtoItemValor
            val formatador: NumberFormat = NumberFormat
                .getCurrencyInstance(Locale("pt", "br"))
            val valorEmMoeda: String = formatador.format(produto.valor)
            valor.text = valorEmMoeda

            val visibilidade = if(produto.imagem != null){
                View.VISIBLE
            } else {
                View.GONE
            }

            binding.imageView.visibility = visibilidade
            binding.imageView.tryToLoad(produto.imagem)
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val inflater = LayoutInflater.from(context)
        val binding = ProdutoItemBinding.inflate(inflater, parent, false)
        return ViewHolder(binding)
        // val inflater = LayoutInflater.from(context)
        // val view = inflater.inflate(R.layout.produto_item, parent, false)
        // return ViewHolder(view)
    }

    override fun getItemCount(): Int = this.produtos.size

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val produto = produtos[position]
        holder.vincula(produto)
    }

    fun atualiza(listaProdutos: List<Produto>) {
        this.produtos.clear()
        this.produtos.addAll(listaProdutos)
        notifyDataSetChanged()
    }

}
