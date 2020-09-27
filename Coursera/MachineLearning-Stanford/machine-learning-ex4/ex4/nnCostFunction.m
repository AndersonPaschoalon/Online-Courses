function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1); %tamanho do training set

% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m
%
% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.
%
% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculo do custo J()
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
JLr = 0; %custo logistic regression
JReg = 0; %valor da regularizacao
K = num_labels; %numero de labels (valores de saida possiveis)
hth = zeros(K,1); %funcao logistica
oneVet = ones(K,1); %vetor de uns
Hth = zeros(m,K); % matriz dos falores das funcoes logisticas
i = 0; %contador do training set
k = 0; %contador do numero de labels

%calculo dos valores de hth da rede neural
%%Layer1
a1 = [ones(m,1) X];
%%Layer2
z2 = a1*(Theta1');
a2 = [ones(m,1) sigmoid(z2)];
%%Layer3
z3 = a2*(Theta2');
HTh = sigmoid(z3);

%Calculo do custo sem regularizacao
for i = 1:m
        %primeiramente os valores de y devem ser regularizados
        yVet = zeros(K, 1);
        yVet(y(i)) = 1;
        hth = HTh(i,:)';
        JLr = JLr + sum(-yVet.*log(hth) - (oneVet - yVet).*log(oneVet - hth)); 
endfor
JLr = JLr/m;

% calculo da regularizacao
ThetaTemp = Theta1(:,2:end).^2;
JReg = sum(sum(ThetaTemp));
ThetaTemp = Theta2(:,2:end).^2;
JReg = JReg + sum(sum(ThetaTemp));
JReg = (lambda/(2*m))*JReg;

%custo
J = JLr + JReg; 


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculo do gradiente
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
t = 0; % contador para o training set
Delta2 = zeros(size(Theta2)); % R(10, 26)
Delta1 = zeros(size(Theta1)); % R(25, 401)
ThetaReg1 = zeros(size(Theta1));
ThetaReg1 = [zeros(size(Theta1, 1),1) Theta1(:,2:end)];
ThetaReg2 = zeros(size(Theta2));
ThetaReg2 = [zeros(size(Theta2, 1),1) Theta2(:,2:end)];

for t = 1:m
        %passo1
        a1 = [1; X(t,:)']; % R(401 x 1)
        %passo2
        z2 = Theta1*a1; % R(25 x 401) * R(401 x 1)
        a2 = [1; sigmoid(z2)]; % R(26 x 1)
        %passo3
        z3 = Theta2*a2; % R(10 x 26) * R(26 x 1)
        a3 = sigmoid(z3); % R(10 x 1)
        
        %Calculo de yVet
        yVet = zeros(K,1);
        yVet(y(t)) = 1; % R(10 x 1)
        
        %Calculo do erro
        delta3 = a3 - yVet; % R(10 x 1)
        delta2 = ((Theta2')*delta3).*(a2.*( ones(size(a2)) - a2)); 
                % R(26x10)*R(10x1) .* R(26x1)  
        
        %Calculo do Delta
        Delta2 = Delta2 + delta3*(a2'); % R(10x26) R(10x1)*R(1X26)
        Delta1 = Delta1 + delta2(2:end)*(a1'); % R(401x25) R(25,1)*R(1x401)
        
endfor

D2 = (1/m)*Delta2 + (lambda/m)*ThetaReg2;
D1 = (1/m)*Delta1 + (lambda/m)*ThetaReg1;

Theta1_grad = D1;
Theta2_grad = D2;


% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];


end
