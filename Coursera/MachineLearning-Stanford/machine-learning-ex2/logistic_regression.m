% jval 	: função de custo 
% gradient	: 	
function [jVal, gradient] = costFunction(theta)
	
	%printf("Algoritimo built-in de Logistic Regression \n")

	jVal = (theta(1) - 5)^2 + (theta(2) - 5)^2;
	
	%  duas linhas, uma coluna
	gradient = zeros(2,1);
	
	gradient(1) = 2*(theta(1) - 5);

	gradient(2) = 2*(theta(2) - 5);
	
endfunction

options = optimset('GradObj', 'on', 'MaxIter', '100' );
	
initialTheta = zeros(2,1);
	
[optTheta, functionVal, exitFlag] = fminunc(@costFunction, initialTheta, options)


