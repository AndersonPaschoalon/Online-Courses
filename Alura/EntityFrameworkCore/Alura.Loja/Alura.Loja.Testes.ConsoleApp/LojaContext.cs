using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

namespace Alura.Loja.Testes.ConsoleApp
{
    public class LojaContext : DbContext
    {

        public DbSet<Produto> Produtos { get; set; }
        public DbSet<Compra> Compras { get; set; }
        public DbSet<Promocao> Promocoes { get; set; }

        public DbSet<PromocaoProduto> PromocoesProdutos { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // criando chave primaria composta
            modelBuilder
                .Entity<PromocaoProduto>()
                .HasKey(prpd => new { prpd.PromocaoId, prpd.ProdutoId});

            /*
            modelBuilder
                .Entity<PromocaoProduto>()
                .HasOne(prpd => prpd.Produto)
                .WithMany(pd => pd.Promocoes)
                .HasForeignKey(prpd => prpd.ProdutoId);

            modelBuilder
                .Entity<PromocaoProduto>()
                .HasOne(prpd => prpd.Promocao)
                .WithMany(pr => pr.Produtos)
                .HasForeignKey(prpd => prpd.PromocaoId);
             */

            base.OnModelCreating(modelBuilder);
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlServer("Server=(localdb)\\mssqllocaldb;Database=LojaDB;Trusted_Connection=true;");
        }

    }
}