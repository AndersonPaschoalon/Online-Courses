
%training set
s1 = 2;
s2 = 5;
s3 = 2;
m = 6;
X = rand(m, s1);
Theta1 = rand(s2, s1 + 1);
Theta2 = rand(s3, s2 + 1);

%X = [2 3; 1 2; 4 5; 7 8; 9 10; 3 4];
%Theta1 = [1 2 1; 2 1 1 ; 1 2 2 ; 2 1 2 ; 1 2 1];
%Theta2 = [1 3 5 7 9 11; 2 4 6 8 10 12]; 

m = size(X, 1); %tamanho do training set 
n = size(X, 2); % numero de features


% passo 1: a^(1) = x
a1 = [ones(m, 1) X];

% passo 2
z2 = a1*(Theta1');
a2 = sigmoid(z2);
a2 = [ones(m, 1) a2];

% passo 3
z3 = a2*(Theta2');
a3 = sigmoid(z3);

hTh = a3



