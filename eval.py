from flask import Flask
#from problem import *
import tests
import requests


app = Flask(__name__)

@app.route('/')
def hello():
    return {"hello": "world"}


@app.route('/compare/<int:size>')
def eval(size):
    results = tests.compare_algorithms(["alex", "carla"], size)
    
    return results



if __name__ == '__main__':
    app.run(port=5000)


