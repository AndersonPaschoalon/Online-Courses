function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
%C = 1;
%sigma = 0.3;
C = 0;
sigma = 0;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%        simbolo "~=" realiza a operacao logica diferente entre dois valores.
%        se for diferente o valor ser´a "1", se for igual ser´a "0";

x1 = [1 2 1]; %?
x2 = [0 4 -1]; %?
C_values = [0.01 0.03 0.1 0.3 1 3 10 30];
sigma_values = [0.01 0.03 0.1 0.3 1 3 10 30];
min_predictions = 0;
new_predictions = 0;


for i = 1:length(C_values)

  for j = 1:length(sigma_values)
  
  % Train the SVM
  %model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));
  model= svmTrain(X, y, C_values(i), @(x1, x2) gaussianKernel(x1, x2, sigma_values(j) ));
  predictions = svmPredict(model, Xval);
  
    if(i == 1 && j == 1)
      %1o valor calculado para numero de acertos
      min_predictions = mean(double(predictions ~= yval));
      C = C_values(i);
      sigma = sigma_values(j);
      
    else
      %calcula novo numero de acertos
      new_predictions = mean(double(predictions ~= yval));
      
      %se o numero de acertos e menor, o novo valor e selecionado
      if(new_predictions < min_predictions)
        
        min_predictions = new_predictions;
        C = C_values(i);
        sigma = sigma_values(j);
        
      end
    
    end
  
  end

end



% =========================================================================

end
