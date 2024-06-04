package br.com.apaschoalon.math;

public class SimpleMath {

	
	public static Double sum(
			 Double numberOne,
			Double numberTwo){
		return numberOne + numberTwo; 
	}


	public static Double sub(
			Double numberOne,
			Double numberTwo){
		return numberOne - numberTwo; 
	}
	
	public static Double mul(
			Double numberOne,
			Double numberTwo){
		return numberOne * numberTwo; 
	}	

	public static Double div(
			Double numberOne,
			Double numberTwo){
		return numberOne / numberTwo; 
	}	
	
	public static Double sqrt(
			Double numberOne){
		return Math.sqrt(numberOne); 
	}		

	public static Double mean(
			Double numberOne,
			Double numberTwo){

		return (numberOne + numberTwo)/2 ; 	
	}	
	
}
