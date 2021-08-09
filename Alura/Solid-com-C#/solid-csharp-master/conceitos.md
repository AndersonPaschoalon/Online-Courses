# SRP: SINGLE RESPONSABILITY PRINCIPLE

	- Coesão - Ligação, harmonia, união entre as partes

	- DRY: Dont repead yorself.
	- Métodos devem ter uma unica responsabilidade.
	- Classes devem ter uma única responsabilidade.
	- Responsabilidade de método é diferente de uma responsabilidade de classe:
	- Um médodo para existir deve ter uma unica intenção.
	- Uma classe é um agente de mudança. Uma classe deve ter uma unica responsabilidade. 
	Ela deve atender a um único agente de mudança.
	
	- SINGLE SOURCE OF TRUTH
	- Se a coesão for alta, deve haver uma unica fonte de cada informação
	SRP: SINGLE RESPONSABILITY PRINCIPLE
	- SRP: SINGLE RESPONSABILITY PRINCIPLE

# D - Principio da inversão da dependencia

	- É importante que uma classe tenha poucas dependencias de tipos instaveis, 
	e quando isso ocorra é preferivel que ela dependa de uma abstração. 

	- Invesão de controle: a classe controladora não conhece a implementação concreta.

	- Injeção de dependência: a classe controladora não instancia a implementação 
	concreta. Outra classe é responsável por executar a instanciação das implementações 
	concretas da classe, e passa essa instancia através de uma interface para a classe
	controladora. 

# Princípio do Aberto/Fechado 

-	Manter a aplicação fechada para mudanças, e aberta para extensões
-	A ideia é que a quando ocorra demanda de modificações em certas implementações, se criem classes que 
    herdem a mesma interface, e implementem de uma nova forma as funcionalidades.
-	Um metodo para se fazer isso é usando o padraõ decorator. Neste caso, a nova regra de negocio seria 
    criada em uma nova classe, e esta armazenaria uma instancia da classe antiga. A classe nova chamaria os
	metodos da implementação natiga nos casos que a regra de negocio não muda, e refatoraria a nova implementação.
-	Podemos pensar em uma implementação de um protocolo, cuja nova versão muda o padrão de uma das mensagens trocadas.
	Assumindo que metodos criariam as mensagens a serem trocadas, a nova versão do protocolo poderia armazenar 
	uma instancia da versão antiga, e chamaria os metodos das mensagens antigas. Quando fosse necessário chamar 
	os métodos cujas mensagens foram alteradas, a nova classe refatoraria somente esses métodos. 
	Desta forma, seria simples manter a com



# Liskov Substitution Principle

É importante  cumpri as promessas das abstrações
Se uma funcionalidade não existe, ela não deve ser implementada
Uma funcionadalide que não é necessária não deve ser implementada. Return true não é uma boa ideia
CQRS: Command Query Responsability Segregation -> interface para operações de leitura e escrita separadas! 

Ideias centrais para as interfaces
- Cumpra as promessas das abstrações (LSP - Liskov substitution principle)
- Preocupe-se com a coesão e acoplamento das interfaces. Interfaces devem ser estaveis e cumprir com o prometido (ISP)


