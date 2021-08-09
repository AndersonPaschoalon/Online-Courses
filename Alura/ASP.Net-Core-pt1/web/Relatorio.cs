using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace web
{
    public class Relatorio : IRelatorio
    {
        private readonly List<Livro> livros;

        public Relatorio(ICatalogo catalogo)
        {
            this.livros = catalogo.GetLivros();
        }

        public async Task renderHtml(HttpContext context)
        {
            await context.Response.WriteAsync("-- Test 02 -- \r\n");
            foreach (var livro in this.livros)
            {
                await context.Response.WriteAsync($"{livro.Codigo,-10}{livro.Nome,-40}{livro.Preco.ToString("C"),10}\r\n");
            }
        }

    }
}
