using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore.ChangeTracking;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace Alura.Loja.Testes.ConsoleApp
{
    class Program
    {
        static void Main(string[] args)
        {
            bool t1 = false;
            bool t2 = false;
            bool t3 = false;
            bool t4 = true;


            if (t1) TestSqlAdd();
            if (t2) TestSqlDelete();
            if (t3) TestSincronizarModeloDeClasses();
            if (t4) TestRelacao_1paraN();

            Console.WriteLine("Fim");
        }

        private static void TestRelacao_1paraN()
        {
            var p1 = new Produto() {
                Nome = "Suco de Laranja",
                Categoria = "Bebidas",
                PrecoUnitario = 8.79,
                Unidade = "Litros",
            };
            var p2 = new Produto()
            {
                Nome = "Café",
                Categoria = "Bebidas",
                PrecoUnitario = 12.45,
                Unidade = "Gramas",
            };
            var p3 = new Produto(){
                Nome = "Macarrão",
                Categoria = "Alimentos",
                PrecoUnitario = 4.23,
                Unidade = "Litros",
            };

            var promocaoDePascoa = new Promocao();
            promocaoDePascoa.Descricao = "Pascoa Feliz";
            promocaoDePascoa.DataInicio = DateTime.Now;
            promocaoDePascoa.DataTermino = DateTime.Now.AddMonths(3);
            promocaoDePascoa.IncluiProduto(p1);
            promocaoDePascoa.IncluiProduto(p2);
            promocaoDePascoa.IncluiProduto(p3);

            using (var contexto = new LojaContext())
            {
                var serviceProvider = contexto.GetInfrastructure<IServiceProvider>();
                var loggerFactory = serviceProvider.GetService<ILoggerFactory>();
                loggerFactory.AddProvider(SqlLoggerProvider.Create())
;
                  
                contexto.Promocoes.Add(promocaoDePascoa);
                contexto.SaveChanges();

                ExibeEntries(contexto.ChangeTracker.Entries());
            }


        }

        private static void TestSincronizarModeloDeClasses()
        {

            var paoFrances = new Produto();
            paoFrances.Nome = "Pao Frnaces";
            paoFrances.PrecoUnitario = 0.40;
            paoFrances.Unidade = "Unidade";
            paoFrances.Categoria = "Padaria";
            var compra = new Compra();
            compra.Quantidade = 6;
            compra.Produto = paoFrances;
            compra.Preco = paoFrances.PrecoUnitario * compra.Quantidade;


            using (var contexto = new LojaContext())
            {
                var serviceProvider = contexto.GetInfrastructure<IServiceProvider>();
                var loggerFactory = serviceProvider.GetService<ILoggerFactory>();
                loggerFactory.AddProvider(SqlLoggerProvider.Create())
;
                contexto.Compras.Add(compra);
                contexto.SaveChanges();

                ExibeEntries(contexto.ChangeTracker.Entries());
            }

        }

        private static void TestSqlDelete() 
        {
            using (var contexto = new LojaContext())
            {
                var serviceProvider = contexto.GetInfrastructure<IServiceProvider>();
                var loggerFactory = serviceProvider.GetService<ILoggerFactory>();
                loggerFactory.AddProvider(SqlLoggerProvider.Create());

                Console.WriteLine("== ChangeTracker");
                var produtos = contexto.Produtos.ToList();
                ExibeEntries(contexto.ChangeTracker.Entries());

                var p1 = produtos.First();
                contexto.Produtos.Remove(p1);
                ExibeEntries(contexto.ChangeTracker.Entries());
                contexto.SaveChanges();
                ExibeEntries(contexto.ChangeTracker.Entries());
            }


        }

        private static void TestSqlAdd()
        {
            using (var contexto = new LojaContext())
            {
                var serviceProvider = contexto.GetInfrastructure<IServiceProvider>();
                var loggerFactory = serviceProvider.GetService<ILoggerFactory>();
                loggerFactory.AddProvider(SqlLoggerProvider.Create());

                Console.WriteLine("== ChangeTracker");
                var produtos = contexto.Produtos.ToList();
                ExibeEntries(contexto.ChangeTracker.Entries());

                var novoProduto = new Produto()
                {
                    Nome = "Desinfetante",
                    Categoria = "Limpeza",
                    PrecoUnitario = 2.99,
                };
                contexto.Produtos.Add(novoProduto);

                Console.WriteLine("== ChangeTracker");
                ExibeEntries(contexto.ChangeTracker.Entries());

                contexto.SaveChanges();

            }
        }

        private static void ExibeEntries(IEnumerable<EntityEntry>  entries)
        {
            Console.WriteLine("===============================");
            foreach (var item in entries)
            {
                Console.WriteLine(item.Entity.ToString() + " - " + item.State);
            }
        }


    }
}
