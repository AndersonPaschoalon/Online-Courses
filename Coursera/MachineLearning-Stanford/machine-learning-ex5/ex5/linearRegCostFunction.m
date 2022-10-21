function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear 
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the 
%   cost of using theta as the parameter for linear regression to fit the 
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear 
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%

St = 0;
Sm = 0;
n = length(theta); % number of features
i = 0;
j = 0;
hth = 0;

St = sum([0; theta(2:end)].^2);
for i = 1:m
	hth = 0;
	hth = X(i,:)*theta;
	Sm = Sm + (hth - y(i)).^2;
end

J = (1/(2*m))*Sm + (lambda/(2*m))*St;

Sm = 0;
reg = [0; theta(2:end)]*(lambda/m);
for j = 1:n
	Sm = 0;
	St = 0;
	for i = 1:m
		hth = 0;
		hth = X(i,:)*theta;
		Sm = Sm + (hth - y(i))*X(i,j);
	end
	grad(j) = (1/m)*Sm + reg(j);	

end








% =========================================================================

grad = grad(:);

end
