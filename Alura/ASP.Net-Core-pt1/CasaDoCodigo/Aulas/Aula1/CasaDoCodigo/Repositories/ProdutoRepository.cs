using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using CasaDoCodigo.Models;

namespace CasaDoCodigo.Repositories
{
    public class ProdutoRepository : BaseRepository<Produto>, IProdutoRepository
    {

        public ProdutoRepository(ApplicationContext contexto) : base(contexto)
        {
            
        }

        public IList<Produto> GetProdutos()
        {
            return this.dbSet.ToList();

        }

        public void SaveProdutos(List<Livro> livros)
        {
            // insere no db
            foreach (var livro in livros)
            {
               
                if (!this.dbSet.Where(p => p.Codigo == livro.Codigo).Any())
                {
                    this.dbSet.Add(new Produto(livro.Codigo, livro.Nome, livro.Preco));
                }

            }
            this.context.SaveChanges();
        }

    }
}
