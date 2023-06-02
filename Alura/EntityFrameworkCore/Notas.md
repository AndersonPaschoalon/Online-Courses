# Instalação do EntityFramwork

```
Install-Package Microsoft.EntityFrameworkCore.SqlServer -Version 1.1
```

# Instalar pacote de Migrations

```
Install-Package Microsoft.EntityFrameworkCore.Tools -Version 1.1.1
```

# Migrations

A migração é feita em dois passos. 

1. O primeiro passo é registar a migração, utilizando o Add-Migration

2. O Segundo passo pode ser feito de duas formas 

a) Utilizando um script de migração, via comando Script-Migration.
b) A segunda maneira é rodando diratamente, via comando Update-Database.

# Criando Migration

Primeiro vamos criar uma migração para o estado inicial da aplicação:
```
Add-Migration Inicial
```

Vamos criar uma migration para autalizar a tabela Produtos do banco de dados:
```
Add-Migration Unidade
```

Para aplicarmos a migração, comantamos o código do metodo Up da migração Inicial, e executamo o comando :

```
 Update-Database Inicial
```

Em seguida, descomentamos o código, e executamos:

```
 Update-Database 
```

Ele vai executar a migração mais recente, ou seja com nome Unidade.






