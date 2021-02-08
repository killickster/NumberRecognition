import numpy as np

def format_data(number_of_epochs, batch_size, training_data):
    epochs = []
    for i in range(number_of_epochs):
        np.random.shuffle(training_data)
        epochs.append([training_data[k:k+batch_size] for k in range(0,len(training_data), batch_size)])
    return epochs
        

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

def import_training_data(path, delim=','):
    data = np.loadtxt(path, delimiter=delim)
    expected_output = [np.reshape(np.array([1 if x == data[i][0] else 0 for x in range(0,10)]), (10,1)) for i in range(0,data.shape[0])]
    activations = [np.reshape(data[i][1:],(data.shape[1]-1,1))/255 for i in range(0, data.shape[0])]                       
    return list(zip(expected_output, activations))

def import_test_data(path, delim=','):
    data = np.loadtxt(path, delimiter=delim)
    return[(data[i][0], np.reshape(data[i][1:], (data.shape[1]-1,1))/255) for i in range(0,data.shape[0])]