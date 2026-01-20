package org.projetosotelli;

public class SaldoCedula {
	
	private int qtdCedula;
	private Cedula cedula;
	
	/**
	 * Construtor. Classe armazena quantidade de uma certa cedula armazenadas,
	 * e informações sobre a própria cedula.
	 * @param inputCedula cedula que informações serão armazenadas
	 */
	public SaldoCedula(Cedula inputCedula)
	{
		cedula = inputCedula;
		qtdCedula = 0;
	}
	
	/**
	 * Retorna a quantidade de cedulas armazenadas
	 * @return quantidade de cedulas armazenadas
	 */
	public int getQtdCedula(){
		return qtdCedula;
	}	
	/**
	 * Retorna a cedual armazenada
	 * @return cedual armazenada
	 */
	public Cedula getCedula(){
		return cedula;
	}	
	
	// settters
	//public void setQtdCedula(int qtdValor){
	//	qtdCedula = qtdValor;
	//}
	//public void setCedula(Cedula inputCedula){
	//	cedula = inputCedula;
	//}

	/***
	 * Adiciona uma certa quantidade de cedulas
	 * @param qtdValor quantidade de cedulas a ser adicionada
	 */
	public void add(int qtdValor){
		qtdCedula += qtdValor;
	}
	
	/**
	 * Remove uma certa quantidade de cedulas
	 * @param qtdValor quantidade de ceduas a ser removida
	 */
	public void sub(int qtdValor){
		int sub = qtdCedula - qtdValor;
		if(sub>=0)
			qtdCedula=sub;
		else
			System.out.println("**Erro: numero de cedulas não pode ser menor que zero**");
	}
	
}
