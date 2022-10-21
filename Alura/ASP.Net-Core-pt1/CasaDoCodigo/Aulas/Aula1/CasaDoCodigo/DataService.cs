using CasaDoCodigo.Models;
using CasaDoCodigo.Repositories;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;

namespace CasaDoCodigo
{
    public class DataService : IDataService
    {
        private readonly ApplicationContext context;
        private readonly IProdutoRepository produtoRepository;

        public DataService(ApplicationContext context, IProdutoRepository productRepository)
        {
            this.context = context;
            this.produtoRepository = productRepository;
        }

        public void InitializeDB()
        {
            // cria o db
            this.context.Database.EnsureCreated();

            // salva livros
            List<Livro> livros = DataService.GetLivros();
            this.produtoRepository.SaveProdutos(livros);

        }



        private static List<Livro> GetLivros()
        {
            // le o datasource -- json
            var json = File.ReadAllText("livros.json");
            var livros = JsonConvert.DeserializeObject<List<Livro>>(json);
            return livros;
        }
    }
}
