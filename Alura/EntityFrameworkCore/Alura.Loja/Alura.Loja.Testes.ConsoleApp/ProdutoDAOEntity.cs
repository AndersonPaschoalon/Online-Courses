using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alura.Loja.Testes.ConsoleApp
{
    class ProdutoDAOEntity : IProdutoDAO, IDisposable
    {
        private LojaContext contexto;

        public ProdutoDAOEntity()
        {
            this.contexto = new LojaContext();
        }

        public void Adicionar(Produto p)
        {
            this.contexto.Produtos.Add(p);
            this.contexto.SaveChanges();
        }

        public void Atualizar(Produto p)
        {
            this.contexto.Produtos.Update(p);
            this.contexto.SaveChanges();
        }

        public void Dispose()
        {
            this.contexto.Dispose();
        }

        public IList<Produto> Produtos()
        {
            return this.contexto.Produtos.ToList();
        }

        public void Remover(Produto p)
        {
            this.contexto.Produtos.Remove(p);
            this.contexto.SaveChanges();
        }
    }
}
