from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = connectToMySQL('logReg')
app.secret_key = 'secret'

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login_process', methods=['POST'])
def login():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")   
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!") 
    if len(request.form['password']) <4:
        flash('Password must be 4 characters or longer!')

    mysql = connectToMySQL('logReg')
    all_users = mysql.query_db('SELECT * FROM users')

    session['email'] = request.form['email']
    session['first_name'] = all_users[0]['first_name']
    for x in all_users:
        if request.form['email'] == x['email'] and request.form['password'] == x['password']:
            return redirect('/loginsuccess')
        
    flash('DENIED')
    return redirect('/')

@app.route('/loginsuccess')
def loggedin():
    return render_template('/loginsuccess.html')

@app.route('/registration', methods=['POST'])
def create():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")   
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!") 
    if len(request.form['first_name']) < 1:
        flash("First name cannot be blank!")
    if len(request.form['last_name']) < 1:
        flash("Last name cannot be blank!")
    if len(request.form['password']) <3:
        flash('Password must be 3 characters or longer!')
    if request.form['password'] != request.form['confirm_password']:
        flash('Password field must match password confirm field')
    if '_flashes' in session.keys():
        return redirect('/')

    mysql = connectToMySQL('logReg')
    query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password']
    }
    print(data)
    session['email'] = request.form['email']
    return redirect('/registration_success')

@app.route('/registration_success')
def registration_success():
    return render_template('registration_success.html')

# @app.route('/login_process')
# def display():
#     mysql = connectToMySQL('logReg')
#     query = 'SELECT first_name FROM users WHERE email = %(email)s; '
#     data = {
#         'email': session['email']
#     }
#     name = mysql.query_db(query, data)
#     print(name)
#     return render_template('loginsuccess.html', name=name)

if __name__ == "__main__":
    app.run(debug=True)
