from flask import Flask, render_template, url_for,jsonify, request, session, flash, redirect
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'arguments'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/arguments'

mongo = PyMongo(app)


@app.route('/')
def index():
    if 'email' in session:
        return render_template('user.html')
    return render_template('register.html')

@app.route('/index')
def index():
     return render_template('index.html')
           

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['name'],'name':request.form['email'], 'password' : hashpass,'secondpassword' : hashpass})
            session['email'] = request.form['email']
            return redirect(url_for('index'))
        
        return 'That email already exists!'

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user=users.find_one({'name':request.form['email']})
           
    if login_user:
           if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8'))==login_user['password'].encode('utf-8'):
           session['email']=request.form['email']
           return redirect(url_for('index'))
    return 'Invalid email/password combination'

@app.route('/adminarg')
def result():
    return render_template('adminarg.html')

@app.route('/adminargedit')
def result():
    return render_template('adminargedit.html')

@app.route('/adminupload')
def result():
    return render_template('adminupload.html')

@app.route('/adminuser')
def result():
    return render_template('adminuser.html')

@app.route('/product')
def result():
    return render_template('product.html')
           
@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/tandc')
def tandc():
    return render_template('tandc.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/userupload')
def userupload():
    return render_template('userupload.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)