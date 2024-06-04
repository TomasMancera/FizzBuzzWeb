import sqlite3
from flask import Flask,flash, request, jsonify, make_response, render_template, session, redirect, url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps
from my_app.my_app import MyApp
from auth.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "f7ed2785e6464011a6ba65f08e83bbd6"

my_app = MyApp()
user = User()


# Token Decorator
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(f"Token payload: {payload}")  # Para depuración
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert!': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'Alert!': 'Invalid Token'}), 401
        return func(payload,*args, **kwargs)
    return decorated


@app.route('/')
def index():
    """Main route displaying the title of the application."""
    return render_template('sign-up.html')

# Success route after login
@app.route('/authorized')
@token_required
def success(payload):
    return render_template("success.html")

# Sign-up route
@app.route('/register', methods=["POST","GET"])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            if user.SignUp(username, password):
             flash('Username already taken', 'danger')
             redirect(url_for('index'))
            else:
                flash("Username created successfully","success")
                
        except Exception as e:
            # exceptions
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}", 400
    
    return render_template('sign-up.html')

# Login Route
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            if user.login(username, password):
                token = jwt.encode({
                    'user': username,
                    'exp': datetime.utcnow() + timedelta(minutes=10)
                }, app.config['SECRET_KEY'], algorithm="HS256")
                
                response = make_response(redirect(url_for("success")))
                print(f"\nGenerated Token: {token}\n")
                response.set_cookie('token', token, httponly=True, samesite='Strict')
                
                return response
                
            else:
                flash('Invalid username or password!', 'danger')
                return redirect(url_for('login'))
        except Exception as e:
            # Imprimir cualquier excepción que ocurra
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}", 400
    
    return render_template('login.html')

#log-out
@app.route('/logout', methods=["POST","GET"])
@token_required
def logout(payload):
    """Logs out the user by removing the token cookie and adding the token to the blacklist."""
    token = request.cookies.get('token')
    if token:
        response = make_response(redirect(url_for('login')))
        response.set_cookie('token', '', expires=0, httponly=True, samesite='Strict')
        flash('Sesión cerrada con éxito', 'success')
        return response
    return jsonify({'Alert!': 'Token is missing!'}), 401

@app.route('/fizzBuzz/<value>', methods=["GET"])
@token_required
def get_fb(payload,value):
    """Returns the result of get_number for a specific value."""
    result = my_app.get_number(value)
    return result

@app.route('/fizzBuzz/<value>', methods=["POST"])
@token_required
def post_fb(payload,value):
    """Accepts and processes a value for post_number."""
    result = my_app.post_number(value)
    return result

@app.route('/range', methods=["POST"])
@token_required
def get_range(payload):
    """Returns results of get_range for a specified range provided in the POST body."""
    values = request.get_json()
    lower_limit = values["lower_limit"]
    upper_limit = values["upper_limit"]
    result = my_app.get_range(lower_limit, upper_limit)
    return result

@app.route('/fizzBuzz/<value>', methods=["DELETE"])
@token_required
def delete_number(payload, value):
    """Deletes a specific data using delete_data (soft delete) or hard_delete_data for admins."""
    username = payload['user']
    if user.is_admin(username):
        result = my_app.hard_delete_data(value)
        return result
       
    else:
        result = my_app.delete_data(value)
        return result
        


@app.route('/fizzBuzz/<value>', methods=["PUT", "PATCH", "HEAD", "OPTIONS"])
def invalidQuerys(value):
    return "", 400

@app.route('/range', methods=["PUT", "PATCH", "HEAD", "OPTIONS"])
def invalidQuerysRange():
    return "", 400



if __name__ == '__main__':
    #user.add_admin()
    app.run(host='0.0.0.0', port=81)

#todo-- plantilla exito y logout