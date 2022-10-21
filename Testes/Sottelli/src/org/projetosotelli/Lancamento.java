package org.projetosotelli;
import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;

public  class Lancamento {
	private String dataHora;
	private int valor;
	
	private static String getDateTime() {
	    DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
	    Date date = new Date();
	    return dateFormat.format(date);
	}
	
	public Lancamento(int lancamentoValor){
		setValor(lancamentoValor);
	}
	
	// getters
	public String getDataHora()
	{
		return dataHora;
	}
	
	public int getValor()
	{
		return valor;
	}
	
	// setters 
	private void setValor(int lancamentoValor)
	{
		valor = lancamentoValor;
		dataHora = getDateTime();
	}
	
	public void show()
	{
		System.out.println("abstract");
	}
	
	
}
