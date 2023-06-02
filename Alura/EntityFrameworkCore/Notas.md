# Instala��o do EntityFramwork

```
Install-Package Microsoft.EntityFrameworkCore.SqlServer -Version 1.1
```

# Instalar pacote de Migrations

```
Install-Package Microsoft.EntityFrameworkCore.Tools -Version 1.1.1
```

# Migrations

A migra��o � feita em dois passos. 

1. O primeiro passo � registar a migra��o, utilizando o Add-Migration

2. O Segundo passo pode ser feito de duas formas 

a) Utilizando um script de migra��o, via comando Script-Migration.
b) A segunda maneira � rodando diratamente, via comando Update-Database.

# Criando Migration

Primeiro vamos criar uma migra��o para o estado inicial da aplica��o:
```
Add-Migration Inicial
```

Vamos criar uma migration para autalizar a tabela Produtos do banco de dados:
```
Add-Migration Unidade
```

Para aplicarmos a migra��o, comantamos o c�digo do metodo Up da migra��o Inicial, e executamo o comando :

```
 Update-Database Inicial
```

Em seguida, descomentamos o c�digo, e executamos:

```
 Update-Database 
```

Ele vai executar a migra��o mais recente, ou seja com nome Unidade.






