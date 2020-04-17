from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'flask_rest'
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_rest"

mongo = PyMongo(app)

@app.route('/framework', methods=['GET'])
def get_all_frameworks():
    framework = mongo.db.framework 

    output = []

    for q in framework.find():
        output.append({'name' : q['name'], 'language' : q['language']})

    return jsonify({'result' : output})

@app.route('/framework/<name>', methods=['GET'])
def get_one_framework(name):
    framework = mongo.db.framework

    q = framework.find_one({'name' : name})

    if q:
        output = {'name' : q['name'], 'language' : q['language']}
    else:
        output = 'No results found'

    return jsonify({'result' : output})

@app.route('/framework', methods=['POST'])
def add_framework():
    framework = mongo.db.framework 

    name = request.json['name']
    language = request.json['language']

    framework_id = framework.insert({'name' : name, 'language' : language})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'name' : new_framework['name'], 'language' : new_framework['language']}

    return jsonify({'result' : output})

@app.route('/framework/<name>', methods=['PUT'])
def edit_framework(name):
    framework = mongo.db.framework 
    framework.find_one_and_update({"_id":ObjectId("5e9971b50aad7c7cc7942f19")}, {"$set": {"name": name}})
    output = []

    for q in framework.find():
        output.append({'name' : q['name'], 'language' : q['language']})

    return jsonify({'result' : output})

@app.route('/framework/<name>', methods=['DELETE'])
def delete_framework(name):
    framework = mongo.db.framework 
    framework.remove({"name": name})
    
    output = []

    for q in framework.find():
        output.append({'name' : q['name'], 'language' : q['language']})

    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)