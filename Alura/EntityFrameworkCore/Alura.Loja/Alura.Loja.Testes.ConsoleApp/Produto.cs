using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;

namespace Alura.Loja.Testes.ConsoleApp
{
    public class Produto
    {
        public int Id { get;  set; }
        public string Nome { get; set; }
        public string Categoria { get; set; }
        public double PrecoUnitario { get; set; }
        public string Unidade { get; set; }

        // [NotMapped]
        public ICollection<PromocaoProduto> Promocoes { get; set; }

        public override string ToString()
        {
            return $"Produto: {this.Nome}, Categoria:{this.Categoria}, Id:{this.Id}, Preço:{this.PrecoUnitario}";
        }

    }
}