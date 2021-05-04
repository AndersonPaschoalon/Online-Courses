## SRP: SINGLE RESPONSABILITY PRINCIPLE

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



