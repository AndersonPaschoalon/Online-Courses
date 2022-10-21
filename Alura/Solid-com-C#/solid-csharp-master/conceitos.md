# SRP: SINGLE RESPONSABILITY PRINCIPLE

	- Coes�o - Liga��o, harmonia, uni�o entre as partes

	- DRY: Dont repead yorself.
	- M�todos devem ter uma unica responsabilidade.
	- Classes devem ter uma �nica responsabilidade.
	- Responsabilidade de m�todo � diferente de uma responsabilidade de classe:
	- Um m�dodo para existir deve ter uma unica inten��o.
	- Uma classe � um agente de mudan�a. Uma classe deve ter uma unica responsabilidade. 
	Ela deve atender a um �nico agente de mudan�a.
	
	- SINGLE SOURCE OF TRUTH
	- Se a coes�o for alta, deve haver uma unica fonte de cada informa��o
	SRP: SINGLE RESPONSABILITY PRINCIPLE
	- SRP: SINGLE RESPONSABILITY PRINCIPLE

# D - Principio da invers�o da dependencia

	- � importante que uma classe tenha poucas dependencias de tipos instaveis, 
	e quando isso ocorra � preferivel que ela dependa de uma abstra��o. 

	- Inves�o de controle: a classe controladora n�o conhece a implementa��o concreta.

	- Inje��o de depend�ncia: a classe controladora n�o instancia a implementa��o 
	concreta. Outra classe � respons�vel por executar a instancia��o das implementa��es 
	concretas da classe, e passa essa instancia atrav�s de uma interface para a classe
	controladora. 

# Princ�pio do Aberto/Fechado 

-	Manter a aplica��o fechada para mudan�as, e aberta para extens�es
-	A ideia � que a quando ocorra demanda de modifica��es em certas implementa��es, se criem classes que 
    herdem a mesma interface, e implementem de uma nova forma as funcionalidades.
-	Um metodo para se fazer isso � usando o padra� decorator. Neste caso, a nova regra de negocio seria 
    criada em uma nova classe, e esta armazenaria uma instancia da classe antiga. A classe nova chamaria os
	metodos da implementa��o natiga nos casos que a regra de negocio n�o muda, e refatoraria a nova implementa��o.
-	Podemos pensar em uma implementa��o de um protocolo, cuja nova vers�o muda o padr�o de uma das mensagens trocadas.
	Assumindo que metodos criariam as mensagens a serem trocadas, a nova vers�o do protocolo poderia armazenar 
	uma instancia da vers�o antiga, e chamaria os metodos das mensagens antigas. Quando fosse necess�rio chamar 
	os m�todos cujas mensagens foram alteradas, a nova classe refatoraria somente esses m�todos. 
	Desta forma, seria simples manter a com



# Liskov Substitution Principle

� importante  cumpri as promessas das abstra��es
Se uma funcionalidade n�o existe, ela n�o deve ser implementada
Uma funcionadalide que n�o � necess�ria n�o deve ser implementada. Return true n�o � uma boa ideia
CQRS: Command Query Responsability Segregation -> interface para opera��es de leitura e escrita separadas! 

Ideias centrais para as interfaces
- Cumpra as promessas das abstra��es (LSP - Liskov substitution principle)
- Preocupe-se com a coes�o e acoplamento das interfaces. Interfaces devem ser estaveis e cumprir com o prometido (ISP)


