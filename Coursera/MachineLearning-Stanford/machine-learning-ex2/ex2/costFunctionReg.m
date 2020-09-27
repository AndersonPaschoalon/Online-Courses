function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples
n = length(theta); %number of features

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

%init variables
x = zeros(size(theta));
somaGrad = 0;
somaReg = 0;
xth = 0; % theta' * x
hth = 0;
j = 0; % #features
i = 0; % #training
zeroVetH = zeros(1, n-1);
zeroVetV = zeros(m-1, 1);
EyeIn = zeros(m,n);
Eye = eye(m - 1,n - 1);
thetaj = 0;

%cost evaluation
for i = 1:m
	x = X(i,:)';
	xth = theta'*x;
	somaGrad = somaGrad - y(i)*log(sigmoid(xth)) - (1 - y(i))*log(1 - sigmoid(xth));
endfor 

%parameter theta(0) should not be regularized!
for j = 2:n
	somaReg = somaReg + theta(j)*theta(j);
endfor

J = (1/m)*somaGrad + (lambda/(2*m))*somaReg;

%theta evaluation


j = 0;
i = 0;

for j = 1:n
	
	somaGrad = 0;
	for i = 1:m
		x  = X(i,:)';
		xh = theta'*x;
		somaGrad = somaGrad + (sigmoid(xh) - y(i))*x(j);	
	endfor

  % do not compute regularization for theta(0) (when j == 1)
	if( j == 1)
		grad(j) = somaGrad/m;
	else
		grad(j) = somaGrad/m + theta(j)*(lambda/m);	
	endif
	

endfor

% =============================================================

end
