using System.Linq;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using Alura.LeilaoOnline.WebApp.Models;


namespace Alura.LeilaoOnline.WebApp.Dados.EfCore
{
    public class LeilaoDAOComEfCore: ILeilaoDao
    {

        AppDbContext _context;


        public LeilaoDAOComEfCore()
        {
            this._context = new AppDbContext();
        }

        public IEnumerable<Categoria> BuscarCategorias()
        {
            return this._context.Categorias.ToList();
        }

        public IEnumerable<Leilao> BuscarLeiloes()
        {
            return this._context.Leiloes
                .Include(l => l.Categoria)
                .ToList();
        }

        public Leilao BuscarPorId(int id)
        {
            return this._context.Leiloes.First(l => l.Id == id);
        }

        public void Incluir(Leilao leilao)
        {
            this._context.Leiloes.Add(leilao);
            this._context.SaveChanges();
        }

        public void Alterar(Leilao leilao)
        {
            this._context.Leiloes.Update(leilao);
            this._context.SaveChanges();
        }

        public void Excluir(Leilao leilao)
        {
            this._context.Leiloes.Remove(leilao);
            this._context.SaveChanges();
        }

    }
}
