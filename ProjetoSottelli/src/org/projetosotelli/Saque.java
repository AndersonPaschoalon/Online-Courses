package org.projetosotelli;

public class Saque extends Lancamento{
	
	/**
	 * Construtor. Define uma operação de saque executada com sucesso, 
	 * para ser gravada.
	 * @param lancamentoValor
	 */
	public Saque(int lancamentoValor)
	{
		super(lancamentoValor);
	}
	
	/**
	 * Mostra da saida padrão a operação de saque definida nesta classe
	 */
	public void show()
	{
		System.out.println(getDataHora()+"\tSaque\t\t"+getValor());
	}
	
	
}
