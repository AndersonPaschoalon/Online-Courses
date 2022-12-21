# Declarar Servidor Web

Pra adicionar um servidor, devemos declarar um host:
```
IWebHost host;
```
# Instalar dependências

Como a aplicação não é web, o pacote não vem instalado.
Para instalar o pacote, utilizar:

```
Install-Package Microsoft.AspNetCore -Version 2.0.1
```

Instalar o pacote aspNetCore.Mvc

```
Install-Package Microsoft.AspNetCore.Mvc -Version 2.0.2
```

# Model binding no ASP.NET Core

Este artigo explica o que é model binding, como ele funciona e como personalizar seu comportamento.
O que é o model binding

Controladores e Razor páginas funcionam com dados provenientes de solicitações HTTP. Por exemplo, dados de rota podem fornecer uma chave de registro e campos de formulário postados podem fornecer valores para as propriedades do modelo. Escrever código para recuperar cada um desses valores e convertê-los de cadeias de caracteres em tipos .NET seria uma tarefa entediante e propensa a erro. O model binding automatiza esse processo. O sistema de model binding:

* Recupera dados de várias fontes, como dados de rota, campos de formulário e cadeias de caracteres de consulta.
* Fornece os dados para controladores e Razor páginas em parâmetros de método e propriedades públicas.
* Converte dados de cadeia de caracteres em tipos .NET.
* Atualiza as propriedades de tipos complexos.

*Exemplo*

Suponha que você tenha o seguinte método de ação:

```
[HttpGet("{id}")]
public ActionResult<Pet> GetById(int id, bool dogsOnly)
```

E o aplicativo receba uma solicitação com esta URL:

```
https://contoso.com/api/pets/2?DogsOnly=true
```

A associação de modelo passa pelas seguintes etapas depois que o sistema de roteamento seleciona o método de ação:

* Localiza o primeiro parâmetro de GetById, um número inteiro denominado id.
* Examina as fontes disponíveis na solicitação HTTP e localiza id = "2" em dados de rota.
* Converte a cadeia de caracteres "2" em inteiro 2.
* Localiza o próximo parâmetro de GetById, um booliano chamado dogsOnly.
* Examina as fontes e localiza "DogsOnly=true" na cadeia de consulta. A correspondência de nomes não diferencia maiúsculas de minúsculas.
* Converte a cadeia de caracteres "true" no booliano true.

A estrutura então chama o método GetById, passando 2 para o parâmetro id e true para o parâmetro dogsOnly.

No exemplo anterior, os destinos do model binding são parâmetros de método que são tipos simples. 
Destinos também podem ser as propriedades de um tipo complexo. 
Depois de cada propriedade ser associada com êxito, a validação do modelo ocorre para essa propriedade. 
O registro de quais dados estão associados ao modelo, além de quaisquer erros de validação ou de associação, é armazenado em ControllerBase.ModelState ou PageModel.ModelState. 
Para descobrir se esse processo foi bem-sucedido, o aplicativo verifica o sinalizador ModelState.IsValid.

# Execute Result

Estagio depois da action.


