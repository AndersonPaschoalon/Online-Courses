function [media, soma] = mediaSoma(valor1, valor2)
	printf("Calculando a media e a soma\n")
	media = (valor1 + valor2)/2;
	soma = (valor1 + valor2);
endfunction

[v1, v2] = mediaSoma(2, 3);
v1
v2
