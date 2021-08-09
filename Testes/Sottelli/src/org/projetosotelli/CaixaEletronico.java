package org.projetosotelli;
import java.util.Scanner;
import org.projetosotelli.Lancamento;
import java.util.Vector;
import java.lang.Integer;

public class CaixaEletronico {
	
	private Vector listLancamentos = new Vector();
	
	/**
	 * Estrutura que define as cedulas a serem utilizadas, e o saldo
	 * de cada uma. Para o caida eletronico suportar alguma nota nova,
	 * basta adicionar linhas adicionais. O valor das cedulas deve estar
	 * em ordem crescente.
	 */
	private SaldoCedula saldoDasNotas[] = {
			new SaldoCedula(new Cedula(5, "R$ 5,00")),
			new SaldoCedula(new Cedula(10, "R$ 10,00")),
			new SaldoCedula(new Cedula(20, "R$ 20,00")),
			new SaldoCedula(new Cedula(50, "R$ 50,00")),
			new SaldoCedula(new Cedula(100, "R$ 100,00"))
	};

	/**
	 * Mosta na saida padrão uma lista com as cedulas disponíveis no momento.
	 */
	private void mostrarCedulasDisponiveis()
	{
		System.out.print("Cédulas disponiveis:");
		for(int i=0; i<saldoDasNotas.length; i++)
		{
			if(saldoDasNotas[i].getQtdCedula() > 0)
				System.out.print(saldoDasNotas[i].getCedula().getNome()+"  ");
		}
		System.out.print("\n");
	}
	
	/**
	 * Retorna o saldo disponivel no momento
	 * @return saldo disponível
	 */
	private int saldoDisponivel()
	{
		
		int saldo = 0;
		for(int i=0; i<saldoDasNotas.length; i++)
		{
			saldo += saldoDasNotas[i].getQtdCedula()*saldoDasNotas[i].getCedula().getValor();
		}
		return saldo;
	}
	
	/**
	 * Exibe um extrato das operações de saque e deposito realizadas, com data
	 * e hora.
	 */
	public void ExibirExtrato()
	{ 	
		System.out.println("Data e Hora\t\tLancamento\tValor");
		System.out.println("-----------\t\t----------\t-----");
		for(int i=0; i<listLancamentos.size(); i++)
		{	
			((Lancamento)listLancamentos.get(i)).show();
		}		
	}
	
	/**
	 * Exibe a quantidade de cedulas de cada tipo
	 */
	public void ExibirSaldo(){
		System.out.println("Saldo das notas\n---------------");
		for(int i=0; i<saldoDasNotas.length; i++)
		{
			System.out.println(saldoDasNotas[i].getCedula().getNome()+":\t"+saldoDasNotas[i].getQtdCedula());
		}	
	}
	
	/**
	 * Realiza a operação de deposito.
	 * @param reader Scanner para a saida padrão
	 */
	public void RealizaDeposito(Scanner reader){
		int somaValor = 0;
		for(int i=0; i<saldoDasNotas.length; i++)
		{
			System.out.println("Numero de notas de "+saldoDasNotas[i].getCedula().getNome());
			int quantidadeNotas = reader.nextInt();
			saldoDasNotas[i].add(quantidadeNotas);
			somaValor += quantidadeNotas*saldoDasNotas[i].getCedula().getValor();		
		}
		
		//atualiza extrato
		Lancamento novoDep = new Deposito(somaValor);
		listLancamentos.add(novoDep);
		
	}
	
	/**
	 * Procedimento de realização do saque.
	 * @param reader Scanner para a saida padrão
	 */
	public void RealizaSaque(Scanner reader)
	{
		System.out.println("Valor do Saque: ");
		System.out.print("R$ ");
		int valorSaque = reader.nextInt();
		int valorSaqueConst = valorSaque;
		
		if(valorSaqueConst > saldoDisponivel())
		{
			System.out.println("Saldo Insuficiente\nSaldo Disponível:"+saldoDisponivel());
			return;
		}
		
		Vector ans = new Vector();
		for(int i=saldoDasNotas.length-1; i>=0; i--)
		{
			while(valorSaque>=saldoDasNotas[i].getCedula().getValor() &&
					saldoDasNotas[i].getQtdCedula()>0)
			{
				valorSaque -= saldoDasNotas[i].getCedula().getValor();
				saldoDasNotas[i].sub(1);
				ans.add(new Integer(saldoDasNotas[i].getCedula().getValor())); 
			}
		}

		System.out.print("Notas(R$): ");
		for(int i=0; i<ans.size(); i++){
			System.out.print("+"+ans.get(i));
		}
		System.out.println("");		
		
		int soma = 0;
		for(int i=0; i<ans.size(); i++){
			soma += ((Integer)ans.get(i)).intValue();
		}
		
		if(soma!=valorSaqueConst)
		{
			System.out.println("Não é possivel sacar valor especificado.");
			mostrarCedulasDisponiveis();
			return;
		}
		
		//atualiza extrato
		Lancamento novoSaque= new Saque(valorSaqueConst);
		listLancamentos.add(novoSaque);
	}

	/**
	 * Main function do programa
	 * @param args
	 */
	public static void main(String [] args)
	{
		Scanner reader = new Scanner(System.in);
		CaixaEletronico ce = new CaixaEletronico();
		boolean quit = false;
		
		while(true)
		{
			System.out.println("\nEscolha a operação que deseja fazer: " +
					"\n1 Realizar deposito\n2 Realizar saque"+
					"\n3 Exibir extrato do caixa eletrônico"+
					"\n4 Exibir saldo do caixa eletrônico\n5 Sair");
			System.out.print("> ");
			int n = reader.nextInt();
			switch (n)
			{
				case 1:
					ce.RealizaDeposito(reader);
					break;
				case 2:
					ce.RealizaSaque(reader);
					break;
				case 3:
					ce.ExibirExtrato();
					break;
				case 4:
					ce.ExibirSaldo();
					break;
				case 5:
					quit = true;
					break;
				default:
					System.out.println("Invalid option "+n);
					break;
			}
			if(quit)
			{
				System.out.println("Fim da operação");
				break;
			}
		}
		reader.close();
	}
	
	

}
