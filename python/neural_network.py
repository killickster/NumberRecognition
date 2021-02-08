import importlib
import random
import numpy as np

data_importer = importlib.import_module("import_data")

class NeuralNet:
	#This contructor takes in a list of sizes for each layer of the nerual network
	def __init__(self, layers):
		self.numberOfLayers = len(layers)
		self.numberOfInputs = layers[0]
		self.weights = [np.random.randn(y,x) for x,y in zip(layers[:-1], layers[1:])]
		self.thresholds = [np.random.randn(size,1) for size in layers[1:]]
		pass

	    
	    #Calculates output of the nerual net based upon input contained in values
	def calculate_output(self, values):
		
		if(len(values) < self.numberOfInputs):
			raise ValueError(
				"size of input and size of first layer of neural network must be the same"
				)
		
		for weight, threshold in zip(self.weights, self.thresholds):
			values = np.dot(weight, values) + threshold
			values = self.sigmoid(values)
			print(values.shape)

		print(values)
		return np.argmax(values)


	def train_network(self, batch_size, number_of_batches, eta):
		training_data = data_importer.load_data()
		n = len(training_data)
		for i in range(number_of_batches):
			random.shuffle(training_data)
			batches = [training_data[x:x+batch_size] for x in range(0,n,batch_size)]
			for batch in batches:
				self.update_with_batch(batch, eta)


	def update_with_batch(self, batch, eta):
		nabla_b = [np.zeros(b.shape) for b in self.thresholds]
		nabla_w = [np.zeros(w.shape) for w in self.weights]

		for x, y in batch:
			delta_nabla_b, delta_nabla_w = self.backprop(x,y)
			for b, db in zip(nabla_b, delta_nabla_b):
				nabla_b = [nb + d_nb for nb, d_nb in zip(nabla_b, delta_nabla_b)]
				nabla_w = [nw + d_nw for nw, d_nw in zip(nabla_w, delta_nabla_w)]
		self.weights = [w-(eta/len(batch))*nw for w,nw in zip(self.weights, nabla_w)]
		self.thresholds = [b-(eta/len(batch))*nb for b,nb in zip(self.thresholds, nabla_b)]


	def backprop(self,x,y):
		nabla_b = [np.zeros(b.shape) for b in self.thresholds]
		nabla_w = [np.zeros(w.shape) for w in self.weights]
		activation = x
		activations = [x]
		zs = []
		for w,b in zip(self.weights, self.thresholds):
			z = np.dot(w,activation) + b
			zs.append(z)
			activation = self.sigmoid(z)
			activations.append(activation)

		delta = self.cost_derivative(activation[-1], y) * self.sigmoid_prime(zs[-1])

		nabla_b[-1] = delta
		nabla_w[-1] = np.dot(delta, activations[-2].transpose())
		
		for l in range(2, self.numberOfLayers):
			delta = np.dot(self.weights[-l+1].transpose(), delta) * self.sigmoid_prime(zs[-l]) 
			nabla_b[-l] = delta
			nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())

		return (nabla_b, nabla_w)


	def cost_derivative(self, activation, y):
		return activation - y

	
	def sigmoid(self, z):
		return 1/(1+np.exp(-z))


	def sigmoid_prime(self,z):
		return self.sigmoid(z) * (1-self.sigmoid(z))



		








