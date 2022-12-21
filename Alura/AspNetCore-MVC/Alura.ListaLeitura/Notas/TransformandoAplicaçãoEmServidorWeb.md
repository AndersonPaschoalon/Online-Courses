# Declarar Servidor Web

Pra adicionar um servidor, devemos declarar um host:
```
IWebHost host;
```
# Instalar depend�ncias

Como a aplica��o n�o � web, o pacote n�o vem instalado.
Para instalar o pacote, utilizar:

```
Install-Package Microsoft.AspNetCore -Version 2.0.1
```

Instalar o pacote aspNetCore.Mvc

```
Install-Package Microsoft.AspNetCore.Mvc -Version 2.0.2
```

# Model binding no ASP.NET Core

Este artigo explica o que � model binding, como ele funciona e como personalizar seu comportamento.
O que � o model binding

Controladores e Razor p�ginas funcionam com dados provenientes de solicita��es HTTP. Por exemplo, dados de rota podem fornecer uma chave de registro e campos de formul�rio postados podem fornecer valores para as propriedades do modelo. Escrever c�digo para recuperar cada um desses valores e convert�-los de cadeias de caracteres em tipos .NET seria uma tarefa entediante e propensa a erro. O model binding automatiza esse processo. O sistema de model binding:

* Recupera dados de v�rias fontes, como dados de rota, campos de formul�rio e cadeias de caracteres de consulta.
* Fornece os dados para controladores e Razor p�ginas em par�metros de m�todo e propriedades p�blicas.
* Converte dados de cadeia de caracteres em tipos .NET.
* Atualiza as propriedades de tipos complexos.

*Exemplo*

Suponha que voc� tenha o seguinte m�todo de a��o:

```
[HttpGet("{id}")]
public ActionResult<Pet> GetById(int id, bool dogsOnly)
```

E o aplicativo receba uma solicita��o com esta URL:

```
https://contoso.com/api/pets/2?DogsOnly=true
```

A associa��o de modelo passa pelas seguintes etapas depois que o sistema de roteamento seleciona o m�todo de a��o:

* Localiza o primeiro par�metro de GetById, um n�mero inteiro denominado id.
* Examina as fontes dispon�veis na solicita��o HTTP e localiza id = "2" em dados de rota.
* Converte a cadeia de caracteres "2" em inteiro 2.
* Localiza o pr�ximo par�metro de GetById, um booliano chamado dogsOnly.
* Examina as fontes e localiza "DogsOnly=true" na cadeia de consulta. A correspond�ncia de nomes n�o diferencia mai�sculas de min�sculas.
* Converte a cadeia de caracteres "true" no booliano true.

A estrutura ent�o chama o m�todo GetById, passando 2 para o par�metro id e true para o par�metro dogsOnly.

No exemplo anterior, os destinos do model binding s�o par�metros de m�todo que s�o tipos simples. 
Destinos tamb�m podem ser as propriedades de um tipo complexo. 
Depois de cada propriedade ser associada com �xito, a valida��o do modelo ocorre para essa propriedade. 
O registro de quais dados est�o associados ao modelo, al�m de quaisquer erros de valida��o ou de associa��o, � armazenado em ControllerBase.ModelState ou PageModel.ModelState. 
Para descobrir se esse processo foi bem-sucedido, o aplicativo verifica o sinalizador ModelState.IsValid.

# Execute Result

Estagio depois da action.


