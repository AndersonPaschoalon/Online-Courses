using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alura.Loja.Testes.ConsoleApp
{
    public class Promocao
    {
        public int Id { get; set; }
        public string Descricao { get;  set; }
        public DateTime DataInicio { get;  set; }
        public DateTime DataTermino { get;  set; }
        public ICollection<PromocaoProduto> Produtos { get; set; }

        public Promocao()
        {
            this.Produtos = new List<PromocaoProduto>();
        }
        

        internal void IncluiProduto(Produto produto)
        {
            this.Produtos.Add(new PromocaoProduto() { Produto = produto });
        }
    }
}
