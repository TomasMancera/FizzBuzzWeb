import sqlite3
from flask import Flask, request,jsonify
from my_app.my_app import MyApp



app = Flask(__name__)
my_app = MyApp()


@app.route('/')
def index():
   
    return '<h2>FizzBuzzWeb</h2>'

@app.route('/fizzBuzz/<value>', methods = ["GET"])
def get_fb(value):
    result = my_app.get_number(value)
    return result

@app.route('/fizzBuzz/<value>', methods = ["POST"])
def post_fb(value):
    result = my_app.post_number(value)
    return result

@app.route('/range', methods = ["POST"])
def get_range():
    values = request.get_json()
    lower_limit = values["lower_limit"]
    upper_limit = values["upper_limit"]
    result = my_app.get_range(lower_limit,upper_limit)
    return result

@app.route('/fizzBuzz/<value>', methods = ["DELETE"])
def delete_number(value):
    result = my_app.delete_data(value)
    return result
      
app.run(host='0.0.0.0', port=81)
