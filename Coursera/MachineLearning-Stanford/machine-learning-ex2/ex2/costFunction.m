function [J, grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Note: grad should have the same dimensions as theta
%

%vars: init
n = length(theta);
xh = 0; %temp - sigmoid arg 
x = zeros(size(theta));
sum = 0; %J parcial
i = 0;
j = 0;
sum = 0;

for i = 1:m
	x = X(i,:)';
	xh = theta'*x;
	sum = sum - y(i)*log(sigmoid(xh)) - (1 - y(i))*log(1 - sigmoid(xh));
endfor 
J = sum/m;

for j = 1:n
	
	sum = 0;
	for i = 1:m
		x  = X(i,:)';
		xh = theta'*x;
		sum = sum + (sigmoid(xh) - y(i))*x(j);	
	endfor

	grad(j) = sum/m;

endfor


% =============================================================

end
