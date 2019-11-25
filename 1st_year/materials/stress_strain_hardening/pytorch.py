import numpy as np
import matplotlib.pyplot as plt

def sample_linear_data(m=20): 
    ground_truth_w = 2.3 # slope
    ground_truth_b = -8 ##intercept
    X = np.random.randn(m)##
    Y = ground_truth_w*X +ground_truth_b ## 
    return X, Y #returns X (the input) and Y (labels)

def plot_data(X, Y):
    plt.figure()
    plt.scatter(X, Y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
m=10
X, Y = sample_linear_data(m)
print(X)
print(len(X))
print(type(X))
print(Y)
plot_data(X,Y)
