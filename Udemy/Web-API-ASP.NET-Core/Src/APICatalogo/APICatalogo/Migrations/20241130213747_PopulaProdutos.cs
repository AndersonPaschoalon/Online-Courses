using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace APICatalogo.Migrations
{
    /// <inheritdoc />
    public partial class PopulaProdutos : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder mb)
        {
            mb.AlterColumn<string>(
                name: "ImagemUrl",
                table: "Produtos",
                type: "varchar(300)",
                maxLength: 300,
                nullable: false,
                oldClrType: typeof(int),
                oldType: "int",
                oldMaxLength: 300)
                .Annotation("MySql:CharSet", "utf8mb4");

            mb.AlterColumn<string>(
                name: "Descricao",
                table: "Produtos",
                type: "varchar(300)",
                maxLength: 300,
                nullable: false,
                oldClrType: typeof(int),
                oldType: "int",
                oldMaxLength: 300)
                .Annotation("MySql:CharSet", "utf8mb4");

            mb.Sql("INSERT INTO Produtos(Nome,Descricao,Preco,ImagemUrl,Estoque,DataCadastro,CategoriaId)" +
                "VALUES('Coca-Cola Diet','Refrigerante de Cola 350 ml',5.45,'cocacola.jpg',50,now(),1)");

            mb.Sql("INSERT INTO Produtos(Nome,Descricao,Preco,ImagemUrl,Estoque,DataCadastro,CategoriaId)" +
                "VALUES('Lanche de Atum','Lanche de Atum com maionese',8.50,'atum.jpg',10,now(),2)");

            mb.Sql("INSERT INTO Produtos(Nome,Descricao,Preco,ImagemUrl,Estoque,DataCadastro,CategoriaId)" +
               "VALUES('Pudim 100 g','Pudim de leite condensado 100g',6.75,'pudim.jpg',20,now(),3)");

        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder mb)
        {
            mb.AlterColumn<int>(
                name: "ImagemUrl",
                table: "Produtos",
                type: "int",
                maxLength: 300,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "varchar(300)",
                oldMaxLength: 300)
                .OldAnnotation("MySql:CharSet", "utf8mb4");

            mb.AlterColumn<int>(
                name: "Descricao",
                table: "Produtos",
                type: "int",
                maxLength: 300,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "varchar(300)",
                oldMaxLength: 300)
                .OldAnnotation("MySql:CharSet", "utf8mb4");

            mb.Sql("DELETE FROM Produtos");
        }
    }
}
