using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace web
{
    public class Catalogo : ICatalogo
    {
        public Catalogo()
        {
        }

        public List<Livro> GetLivros()
        {
            // criar livros
            var livros = new List<Livro>();
            livros.Add(new Livro("001", "O Senhor dos Aneis", 33.33m));
            livros.Add(new Livro("002", "O Silmarilion", 23.50m));
            livros.Add(new Livro("003", "Contos Inacabados", 28.00m));
            return livros;
        }
    }
}
