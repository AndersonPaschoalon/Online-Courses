function [J, grad] = cofiCostFunc(params, Y, R, num_users, num_movies, ...
                                  num_features, lambda)
%COFICOSTFUNC Collaborative filtering cost function
%   [J, grad] = COFICOSTFUNC(params, Y, R, num_users, num_movies, ...
%   num_features, lambda) returns the cost and gradient for the
%   collaborative filtering problem.
%

% Unfold the U and W matrices from params
X = reshape(params(1:num_movies*num_features), num_movies, num_features);
Theta = reshape(params(num_movies*num_features+1:end), ...
                num_users, num_features);

            
% You need to return the following values correctly
J = 0;
X_grad = zeros(size(X));
Theta_grad = zeros(size(Theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost function and gradient for collaborative
%               filtering. Concretely, you should first implement the cost
%               function (without regularization) and make sure it is
%               matches our costs. After that, you should implement the 
%               gradient and use the checkCostFunction routine to check
%               that the gradient is correct. Finally, you should implement
%               regularization.
%
% Notes: X - num_movies  x num_features matrix of movie features
%        Theta - num_users  x num_features matrix of user features
%        Y - num_movies x num_users matrix of user ratings of movies
%        R - num_movies x num_users matrix, where R(i, j) = 1 if the 
%            i-th movie was rated by the j-th user
%
% You should set the following variables correctly:
%
%        X_grad - num_movies x num_features matrix, containing the 
%                 partial derivatives w.r.t. to each element of X
%        Theta_grad - num_users x num_features matrix, containing the 
%                     partial derivatives w.r.t. to each element of Theta
%

%init
i = 0;
j = 0;
theta_jT = zeros(1,num_features);
x_i = zeros(num_features,1);
sumation = 0;
sumArg = 0;

fprintf(".");

for i = 1:num_movies
        x_i = X(i,:)';
        for j = 1:num_users
                
                if( R(i,j) == 1)
                        theta_jT = Theta(j,:);
                        sumArg = (theta_jT*x_i - Y(i,j))^2;
                        sumation = sumation + sumArg;
                end
                
        end

end
J = sumation/2;

fprintf(".");
%AQUI E CALCULO NUMERICO CACETE!!!
for i = 1:num_movies
        x_i = X(i,:)';
        s = zeros(1,num_users);
        for k = 1:num_features
                for j = 1:num_users
                        if(R(i,j) == 1)
                                theta_jT = Theta(j,:);
                                s(j) = (theta_jT*x_i - Y(i,j))*Theta(j,k);
                        end
                end
                X_grad(i,k) = sum(s);
        end
end

fprintf(".");
for j = 1:num_users
        theta_jT = Theta(j,:);
        s = zeros(1,num_movies);
        for k = 1:num_features
                for i = 1:num_movies
                        if(R(i,j) == 1)
                                x_i = X(i,:)';
                                s(i) = (theta_jT*x_i -Y(i,j) )*X(i,k);
                        end
                end
                Theta_grad(j,k) = sum(s);
        end
end

fprintf(".");
%regularization
%Cost
regArg1 = (lambda/2)*sum(sum((Theta.^2)));
regArg2 = (lambda/2)*sum(sum((X.^2)));
J = J + regArg1 + regArg2;
%Gradient
X_grad = X_grad + lambda*X;
Theta_grad = Theta_grad + lambda*Theta;












% =============================================================

grad = [X_grad(:); Theta_grad(:)];

end
