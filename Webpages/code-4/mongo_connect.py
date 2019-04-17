from flask import Flask
from flask.ext.pymongo import PyMongo
app=Flask(__name__)

app.config['MONGO_DBNAME']='arguments'
app.config['MONGO_URI']='mongodb://localhost:27017/arguments'

mongo=PyMongo(app)

@app.route('/add')
def add():
    user=mongo.db.users
    user.insert({'name':'Konstantina'})
    return 'Added User'

if __name_=='__main__':
    app.run(debug==True)