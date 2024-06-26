package br.com.andersonp.orgs.ui.recyclerview.adapter

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import br.com.andersonp.orgs.R
import br.com.andersonp.orgs.model.Produto

class ListaProdutosAdapter(
    private val context: Context,
    produtos: List<Produto>
) : RecyclerView.Adapter<ListaProdutosAdapter.ViewHolder>() {

    private val produtos = produtos.toMutableList()

    class ViewHolder(view: View): RecyclerView.ViewHolder(view) {
        fun vincula(produto: Produto) {
            val nome =  itemView.findViewById<TextView>(R.id.produto_item_nome)
            nome.text = produto.nome

            val descricao =  itemView.findViewById<TextView>(R.id.produto_item_descricao)
            descricao.text = produto.descricao

            val valor =  itemView.findViewById<TextView>(R.id.produto_item_valor)
            valor.text = produto.valor.toPlainString()
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val inflater = LayoutInflater.from(context)
        val view = inflater.inflate(R.layout.produto_item, parent, false)
        return ViewHolder(view)
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
