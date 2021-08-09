package org.projetosotelli;

public class Deposito extends Lancamento{
	
	public Deposito(int lancamentoValor)
	{
		super(lancamentoValor);
	}
	
	public void show()
	{
		System.out.println(getDataHora()+"\tDeposito\t"+getValor());
	}
	
	// test
	public static void main(String [] args)
	{
		Deposito dd = new Deposito(23);
		dd.show();
	}

}
