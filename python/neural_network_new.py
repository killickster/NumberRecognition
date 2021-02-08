import numpy as np

#Defines structure of the neural network
class NeuralNetwork:
    
    def __init__(self,layer_sizes):
        '''Randomly initalizes weights and biasis for 
        neural network with structure defined by layer_sizes'''
        self.num_layers = len(layer_sizes)
        self.weights= [np.random.randn(layer[1],layer[0])for layer in zip(layer_sizes[:-1], layer_sizes[1:])]
        self.biasis = [np.random.randn(layer,1) for layer in layer_sizes[1:]]
    
    def calculate_output(self, input_vector):
        '''Calculates output vector from some input vector'''
        if(input_vector.shape[0] != self.weights[0].shape[1]):
            raise ValueError("Size of input vector must be the same as the size of the first layer of the neural network")
        output_vector = input_vector
        for weight, bias in zip(self.weights, self.biasis):
            output_vector = sigmoid(np.dot(weight,output_vector) + bias)
        return output_vector

    def train_network(self, training_data, eta, test_data):
        epoch_num = 0
        for epoch in training_data:
            epoch_num += 1
            i=0
            print("epoch", epoch_num)
            for batch in epoch:                
                self.update_with_batch(batch, eta)
                if i%100 == 0:
                    print(test_network(self, test_data))
                i+=1
            
    def update_with_batch(self, batch, eta):
        nabla_biasis = [np.zeros(bias.shape) for bias in self.biasis]
        nabla_weights = [np.zeros(weight.shape) for weight in self.weights]
        for expected_output, activation in batch:
            delta_nabla_biasis, delta_nabla_weights = self.backprop(activation, expected_output)
            nabla_biasis = [nb + nbd for nb,nbd in zip(nabla_biasis, delta_nabla_biasis)]
            nabla_weights = [nw + nwd for nw,nwd in zip(nabla_weights, delta_nabla_weights)]
        self.weights = [w - (eta/len(batch))*nw for w, nw in zip(self.weights, nabla_weights)]
        self.biasis = [b - (eta/len(batch))*nb for b, nb in zip(self.biasis, nabla_biasis)]
        
        
    def backprop(self, activation, expected_output):
        nabla_b = [np.zeros(b.shape) for b in self.biasis]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        
        activation = activation
        activations = [activation]
        zs = []
        
        for b, w in zip(self.biasis, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        delta = performance_derivative(activations[-1], expected_output) * sigmoid_derivative(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_derivative(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta)*sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)
        
        
        
def sigmoid(value):
    return 1/(1 + np.exp(-value)) 

def sigmoid_derivative(value):
    return sigmoid(value)*(1-sigmoid(value)) 

def calculate_performance(vector1, vector2):
    '''Used to signal how good the neural network performed'''
    return np.sum(vector1-vector2)
    
def performance_derivative(vector1, vector2):
    return (vector1-vector2)

def test_network(neural_network, test_data):
    """function to be used to test 
    the percentage of predictions the neural
    network got correct"""
    total_trials = 0
    correct_trials = 0
    output_values = [np.argmax(neural_network.calculate_output(vector[1])) for vector in test_data]
    expected_values = list(zip(*test_data))[0]
    for expected, recieved in zip(expected_values,output_values):
        total_trials += 1
        if expected == recieved:
            correct_trials+=1
    return correct_trials/total_trials