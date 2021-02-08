from flask import Flask, request
from flask_restful import Resource, Api
import numpy as np
import importlib
from neural_network_new import NeuralNetwork
from helper_functions import format_data, test_network, import_training_data, import_test_data

image_width = image_height = 28
number_of_image_pixels = image_width * image_height
number_of_classifications = 10    

data_path_base = "/Users/micahkillick/neural_network/"

train_data_path = data_path_base + "mnist_train.csv"
train_data =  import_training_data(train_data_path, delim=',')

test_data_path = data_path_base + "mnist_test.csv"
test_data = import_test_data(test_data_path, delim=",")

nn = NeuralNetwork([number_of_image_pixels, 30, number_of_classifications])

nn.train_network(format_data(3,10,train_data), 3.0, test_data)

app = Flask(__name__)
api = Api(app)


global pixels 

pixels = np.zeros((784,1))	

class Pixel(Resource):
	def put(self, pixel):
		global pixels
		json_data = request.get_json(force=True)	
		pixels[pixel][0] = json_data['data']
		return {pixel: pixels[pixel][0]}

	def get(self, pixel):
		global pixels
		return {pixel: pixels[pixel][0]}


class Show(Resource):
	def delete(self):
		global pixels
		return {'pixel': pixels[0][0]}

class Clear(Resource):
	def delete(self):
		global pixels
		pixels = np.zeros((784,1))
		print(pixels)

class Decode(Resource):
	def get(self):
		global pixels
		print(pixels)
		value = nn.calculate_output(pixels)
		print(np.argmax(value))
		return 




api.add_resource(Pixel, '/pixel/<int:pixel>')
api.add_resource(Show, '/show')
api.add_resource(Decode, '/decode')
api.add_resource(Clear, '/clear')


if __name__ == '__main__':
	app.run(debug=False)
