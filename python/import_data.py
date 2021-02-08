import numpy as np
import matplotlib.pyplot as plt

def load_data():
	train_data = np.loadtxt('./mnist_train.csv', delimiter = ',')

	training_pairs = [(np.array(x[1:]).reshape(784,1)/255,
            vectorize(x[0])) for
                x in train_data]


	return training_pairs

def vectorize(value):
	vec = np.zeros(10)
	vec[int(value)] = 1.0
	return np.reshape(vec, (10,1))
