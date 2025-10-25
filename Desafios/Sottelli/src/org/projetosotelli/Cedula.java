package org.projetosotelli;

public class Cedula {
	private String nome;
	private int valor;
	

	/**
	 * Constructor. Cria uma cedula. 
	 * @param valor valor da cedula.
	 * @param nome nome da cedula, por exemplo "R$ 5,00".
	 */
	public Cedula(int valor, String nome){
		setNome(nome);
		setValor(valor);
	}
	
	/**
	 * Retorna o nome de uma cedula.
	 * @return nome da cedula
	 */
	public String getNome(){
		return nome;
	}
	/**
	 * Retorna o valor da cedula.
	 * @return valor da cedula
	 */
	public int getValor(){
		return valor;	
	}
	
	/**
	 * Redefine o nome de uma cedula
	 * @param cedulaNome
	 */
	private void setNome(String cedulaNome){
		nome = cedulaNome;
	}
	
	/**
	 * Redefine o valor de uma cedula
	 * @param cedulaValor
	 */
	private void setValor(int cedulaValor){
		valor = cedulaValor;
	}
	
}
